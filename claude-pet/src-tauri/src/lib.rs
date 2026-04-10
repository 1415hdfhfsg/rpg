use serde::Serialize;
use sysinfo::System;
use std::sync::Mutex;
use tauri::{AppHandle, Emitter, Manager, State};

#[derive(Debug, Clone, Serialize, PartialEq)]
pub enum PetState {
    Idle,
    Thinking,
    Coding,
    Done,
    Error,
    Greeting,
    Dragged,
}

#[derive(Debug, Clone, Serialize)]
pub struct ClaudeStatus {
    pub state: PetState,
    pub cpu_usage: f32,
    pub is_running: bool,
    pub is_focused: bool,
}

pub struct AppState {
    system: Mutex<System>,
    last_state: Mutex<PetState>,
    idle_seconds: Mutex<u64>,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            system: Mutex::new(System::new_all()),
            last_state: Mutex::new(PetState::Greeting),
            idle_seconds: Mutex::new(0),
        }
    }
}

#[tauri::command]
fn get_claude_status(state: State<AppState>) -> ClaudeStatus {
    let mut sys = state.system.lock().unwrap();
    sys.refresh_processes(sysinfo::ProcessesToUpdate::All, true);

    let mut total_cpu = 0.0_f32;
    let mut is_running = false;

    for process in sys.processes().values() {
        let name = process.name().to_string_lossy().to_lowercase();
        if name.contains("claude") {
            is_running = true;
            total_cpu += process.cpu_usage();
        }
    }

    let mut idle_secs = state.idle_seconds.lock().unwrap();
    let mut last = state.last_state.lock().unwrap();

    let new_state = if !is_running {
        *idle_secs += 3;
        if *idle_secs > 180 {
            PetState::Idle
        } else {
            PetState::Idle
        }
    } else if total_cpu > 50.0 {
        *idle_secs = 0;
        PetState::Thinking
    } else if total_cpu > 10.0 {
        *idle_secs = 0;
        PetState::Coding
    } else {
        *idle_secs += 3;
        if *idle_secs > 180 {
            PetState::Idle
        } else {
            PetState::Coding
        }
    };

    *last = new_state.clone();

    ClaudeStatus {
        state: new_state,
        cpu_usage: total_cpu,
        is_running,
        is_focused: false,
    }
}

#[tauri::command]
fn set_pet_state(state_name: String, app_state: State<AppState>) -> ClaudeStatus {
    let new_state = match state_name.as_str() {
        "idle" => PetState::Idle,
        "thinking" => PetState::Thinking,
        "coding" => PetState::Coding,
        "done" => PetState::Done,
        "error" => PetState::Error,
        "greeting" => PetState::Greeting,
        "dragged" => PetState::Dragged,
        _ => PetState::Idle,
    };

    let mut last = app_state.last_state.lock().unwrap();
    *last = new_state.clone();

    ClaudeStatus {
        state: new_state,
        cpu_usage: 0.0,
        is_running: false,
        is_focused: false,
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![get_claude_status, set_pet_state])
        .setup(|app| {
            let handle = app.handle().clone();

            // Start polling Claude process status every 3 seconds
            std::thread::spawn(move || {
                poll_claude_status(handle);
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running Claude Pet");
}

fn poll_claude_status(app: AppHandle) {
    loop {
        std::thread::sleep(std::time::Duration::from_secs(3));

        let state = app.state::<AppState>();
        let status = {
            let mut sys = state.system.lock().unwrap();
            sys.refresh_processes(sysinfo::ProcessesToUpdate::All, true);

            let mut total_cpu = 0.0_f32;
            let mut is_running = false;

            for process in sys.processes().values() {
                let name = process.name().to_string_lossy().to_lowercase();
                if name.contains("claude") {
                    is_running = true;
                    total_cpu += process.cpu_usage();
                }
            }

            let mut idle_secs = state.idle_seconds.lock().unwrap();
            let mut last = state.last_state.lock().unwrap();

            let new_state = if !is_running {
                *idle_secs += 3;
                PetState::Idle
            } else if total_cpu > 50.0 {
                *idle_secs = 0;
                PetState::Thinking
            } else if total_cpu > 10.0 {
                *idle_secs = 0;
                PetState::Coding
            } else {
                *idle_secs += 3;
                if *idle_secs > 180 {
                    PetState::Idle
                } else {
                    PetState::Coding
                }
            };

            *last = new_state.clone();

            ClaudeStatus {
                state: new_state,
                cpu_usage: total_cpu,
                is_running,
                is_focused: false,
            }
        };

        let _ = app.emit("claude-status-update", &status);
    }
}

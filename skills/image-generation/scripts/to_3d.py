#!/usr/bin/env python3
"""
Convert 2D image to 3D model using Tripo3D API.
Requires TRIPO_API_KEY environment variable.

Usage:
  python3 to_3d.py --input character.png --output model.glb
  python3 to_3d.py --input item.png --format glb --output item.glb
"""

import argparse
import sys
import os
import json
import time
import urllib.request
import urllib.error
import base64

TRIPO_API_BASE = "https://api.tripo3d.ai/v2/openapi"


def get_api_key():
    key = os.environ.get("TRIPO_API_KEY")
    if not key:
        print("Error: TRIPO_API_KEY environment variable not set.", file=sys.stderr)
        print("Get a free API key at: https://platform.tripo3d.ai/", file=sys.stderr)
        print("Then: export TRIPO_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)
    return key


def upload_image(image_path, api_key):
    """Upload an image and return its token."""
    with open(image_path, "rb") as f:
        image_data = f.read()

    ext = os.path.splitext(image_path)[1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(ext.lstrip("."), "image/png")

    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(image_path)

    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + image_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"{TRIPO_API_BASE}/upload",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    return result["data"]["image_token"]


def create_task(image_token, api_key, output_format="glb"):
    """Create a 3D generation task."""
    payload = json.dumps({
        "type": "image_to_model",
        "file": {"type": "image_token", "image_token": image_token},
        "model_version": "default",
        "output_format": output_format,
    }).encode()

    req = urllib.request.Request(
        f"{TRIPO_API_BASE}/task",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    return result["data"]["task_id"]


def poll_task(task_id, api_key, timeout=300):
    """Poll until the task completes."""
    start = time.time()
    while time.time() - start < timeout:
        req = urllib.request.Request(
            f"{TRIPO_API_BASE}/task/{task_id}",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())

        status = result["data"]["status"]
        progress = result["data"].get("progress", 0)
        print(f"  Status: {status} ({progress}%)", file=sys.stderr)

        if status == "success":
            return result["data"]["output"]["model"]
        elif status in ("failed", "cancelled"):
            raise RuntimeError(f"Task {status}: {result['data'].get('error', 'unknown')}")

        time.sleep(5)

    raise TimeoutError(f"Task timed out after {timeout}s")


def download_model(url, output_path):
    """Download the generated 3D model."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(data)

    size_mb = len(data) / (1024 * 1024)
    print(f"Saved: {output_path} ({size_mb:.2f} MB)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Convert 2D image to 3D model")
    parser.add_argument("--input", "-i", required=True, help="Input image path")
    parser.add_argument("--format", "-f", default="glb",
                        choices=["glb", "fbx", "obj", "stl"],
                        help="Output format")
    parser.add_argument("--output", "-o", required=True, help="Output model path")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()

    print(f"Uploading: {args.input}", file=sys.stderr)
    token = upload_image(args.input, api_key)

    print("Creating 3D generation task...", file=sys.stderr)
    task_id = create_task(token, api_key, args.format)
    print(f"Task ID: {task_id}", file=sys.stderr)

    print("Generating 3D model (this may take 30-120s)...", file=sys.stderr)
    model_url = poll_task(task_id, api_key)

    print("Downloading model...", file=sys.stderr)
    download_model(model_url, args.output)

    print(args.output)


if __name__ == "__main__":
    main()

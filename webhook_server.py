from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # GitHub에서 오는 이벤트인지 검증 (옵션)
    if request.headers.get("X-GitHub-Event") == "push":
        # 실제 git pull 실행
        try:
            result = subprocess.run(
                ["git", "-C", "/home/ubuntu/cw_app", "pull", "origin", "main"],
                capture_output=True,
                text=True,
                check=True
            )
            return f"Pulled successfully:\n{result.stdout}", 200
        except subprocess.CalledProcessError as e:
            return f"Error pulling:\n{e.stderr}", 500
    return "No action taken", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

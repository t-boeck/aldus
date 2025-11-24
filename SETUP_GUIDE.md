# Beginner's Setup Guide for Aldus

Welcome! This guide is designed for someone who has never used Docker or GitHub before. We will walk through setting up your computer (Windows or Mac) to run the Aldus Book Maker.

---

## Part 1: Install Necessary Software

### 1. Install Docker Desktop
Docker is a tool that lets you run software in a self-contained "box" (container) so you don't have to install complex dependencies manually.

**For Mac:**
1.  Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
2.  Click **Download for Mac**. Choose "Apple Chip" if you have an M1/M2/M3 Mac, or "Intel Chip" for older Macs.
3.  Open the `.dmg` file and drag the Docker icon to your Applications folder.
4.  Open **Docker** from your Applications. You might see a whale icon in your top menu bar. Wait until it says "Docker Desktop is running".

**For Windows:**
1.  Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
2.  Click **Download for Windows**.
3.  Run the installer and follow the instructions. You may need to restart your computer.
4.  Open **Docker Desktop** from your Start menu. Wait until the bottom left corner says "Engine running" (green).

### 2. Install Git
Git is a tool for downloading code from GitHub.

**For Mac:**
1.  Open the **Terminal** app (Command+Space, type "Terminal").
2.  Type `git --version` and press Enter.
3.  If it's not installed, your Mac will prompt you to install it. Follow the prompts.

**For Windows:**
1.  Go to [git-scm.com/download/win](https://git-scm.com/download/win).
2.  Download the **64-bit Git for Windows Setup**.
3.  Run the installer. You can just keep clicking "Next" through all the options (the defaults are fine).

---

## Part 2: Download the Code

Now we will download the Aldus code to your computer.

1.  Open your command line tool:
    *   **Mac**: Open **Terminal**.
    *   **Windows**: Open **PowerShell** or **Command Prompt**.
2.  Navigate to where you want to save the project (e.g., your Documents folder):
    ```bash
    cd Documents
    ```
3.  "Clone" (download) the repository:
    ```bash
    git clone https://github.com/t-boeck/aldus.git
    ```
4.  Go into the new folder:
    ```bash
    cd aldus
    ```

---

## Part 3: Run the App

This is the magic part. Docker will build the entire application for you.

### 1. Build the "Image"
Think of this as baking a cake. We are following the recipe (`Dockerfile`) to create the application.

Run this command in your terminal (make sure you are inside the `aldus` folder):

```bash
docker build -t aldus .
```

*   **Note**: This might take 5-10 minutes the first time because it's downloading a large system for creating PDFs (LaTeX). Don't worry if it looks like it's stuck downloading; just give it time.
*   **Success**: When it finishes, you'll see a message like `writing image ... done`.

### 2. Run the "Container"
Now we run the app we just built.

**Mac:**
```bash
docker run -p 5000:5000 -v $(pwd)/aldus/output:/app/aldus/output aldus
```

**Windows (PowerShell):**
```bash
docker run -p 5000:5000 -v ${PWD}/aldus/output:/app/aldus/output aldus
```

*   **What this does**:
    *   `-p 5000:5000`: Opens a "door" (port) so you can access the app in your browser.
    *   `-v ...`: Connects the `output` folder inside the app to your computer, so your generated PDFs are saved to your hard drive.

---

## Part 4: Use the App

1.  Open your web browser (Chrome, Safari, Edge).
2.  Type this address: **[http://localhost:5000](http://localhost:5000)**
3.  You should see the Aldus home page!

### Stopping the App
To stop the app, go back to your terminal window and press **Ctrl + C**.

---

## Troubleshooting

*   **"Docker is not running"**: Make sure you opened the Docker Desktop app and the icon is visible in your system tray/menu bar.
*   **"Port already in use"**: This means another program is using port 5000. You can try running on a different port:
    ```bash
    docker run -p 8080:5000 ...
    ```
    Then go to `http://localhost:8080`.

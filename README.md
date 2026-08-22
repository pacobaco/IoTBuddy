# IoT Buddy

**Your environment, in rhythm with you\.**

IoT Buddy is a local\-first, stateful neurofeedback companion that reads your cognitive state \(Delta → Theta → Alpha → Beta → Gamma\) and gently shapes both personal feedback and your smart home environment in real time\.

It combines real\-time EEG processing, circadian\-aware state management, multi\-seat support, and MQTT / Home Assistant integration into a single open\-source system\.

---

## Features

- **State\-Aware Daily Companion**
  Adapts lighting, sound, temperature, and feedback across your full daily rhythm\.
- **Real\-time Neurofeedback**
  Supports live EEG \(BrainFlow, Muse, OpenBCI, etc\.\) or high\-quality simulation\.
- **Multi\-Seat Support**
  Multiple users can run simultaneously with private cognitive states and intelligent shared\-environment arbitration\.
- **Local\-First Architecture**
  All core processing stays on your devices\. No mandatory cloud\.
- **MQTT \+ Home Assistant Native**
  Controls lights, climate, speakers, and scenes through standard open protocols\.
- **Generative Audio**
  Optional OSC output to SuperCollider \(or similar\) for evolving, state\-matched soundscapes\.
- **Open & Extensible**
  Clean modular design ready for customization and research use\.

---

## Quick Start

### 1\. One\-Click Install \(Linux / macOS / Raspberry Pi\)

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/iotbuddy/main/install_iotbuddy.sh | bash
```

### 2\. Manual Install

```bash
git clone https://github.com/yourusername/iotbuddy.git
cd iotbuddy
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3\. Configure

Edit `config/default.yaml` and set your MQTT / Home Assistant details:

```yaml
mqtt:
  host: "homeassistant.local"
  username: "iotbuddy"
  password: "your_password"
```

### 4\. Run \(Simulation Mode\)

```bash
python -m iotbuddy.clients.cli simulate --minutes 5
```

You should see live state changes and corresponding scene recommendations\.

---

## How It Works

1. **Sense** – EEG window or simulated signal
2. **Extract** – Band powers \(Delta, Theta, Alpha, Beta, Gamma\)
3. **Interpret** – Stateful cognitive model \+ circadian bias
4. **Respond**
  - Private neurofeedback \(OSC / audio\)
  - Shared home environment \(via MQTT scenes\)
5. **Arbitrate \(multi\-seat\)** – Intelligent decision when multiple users have different needs

---

## Multi\-Seat Usage

```bash
# Terminal 1
python -m iotbuddy.clients.cli simulate --seat office

# Terminal 2
python -m iotbuddy.clients.cli simulate --seat livingroom
```

Each seat keeps its own state\. The Arbitrator decides the final shared scene \(with night\-time Delta protection\)\.

---

## Home Assistant Scenes

Create these scenes \(or import `scenes/home_assistant.yaml`\):

|Scene           |Purpose                    |
|----------------|---------------------------|
|`buddy_delta`   |Deep sleep protection      |
|`buddy_theta`   |Creative / hypnagogic drift|
|`buddy_alpha`   |Calm relaxed state         |
|`buddy_focus`   |Focused work (Beta)        |
|`buddy_peak`    |Short high-intensity       |
|`buddy_winddown`|Evening transition         |
|`buddy_neutral` |Default fallback           |

---

## Project Structure

```text
iotbuddy/
├── iotbuddy/
│   ├── core.py
│   ├── eeg.py
│   ├── state_machine.py
│   ├── feedback.py
│   ├── iot_bridge.py
│   └── multi_seat/
├── clients/
├── config/
├── scenes/
├── supercolider/
└── scripts/
```

---

## Configuration Overview

Key sections in `config/default.yaml`:

- `mqtt` – Broker connection
- `eeg` – Source \(`simulate | brainflow | etc.`\)
- `feedback` – OSC settings
- `multi_seat` – Timeout and night\-time rules
- `companion` – Learning and summary options

---

## Optional: Real EEG

Change the configuration:

```yaml
eeg:
  source: "brainflow"
  board_id: 0
```

Then restart the companion\. Supported via BrainFlow \(OpenBCI, Muse, and many others\)\.

---

## Optional: Systemd Service \(Linux\)

A service file example is provided in `scripts/`\. Enable it to start IoT Buddy automatically on boot\.

---

## Safety & Design Principles

- Local processing by default
- User always has manual override
- No medical claims
- Transparent state publishing via MQTT
- Explicit consent model for any shared/group features

---

## License

MIT License

## Credits & Inspiration

Built in the spirit of open neurofeedback tooling and local\-first smart home systems\. Inspired by projects exploring real\-time EEG, adaptive environments, and cognitive state awareness\.

**Your environment, in rhythm with you\.**

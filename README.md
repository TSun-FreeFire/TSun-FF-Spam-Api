<div align="center">

# 🚀 TSun SPAM API

### High-Performance Friend Request Processing System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*A powerful, multi-threaded API system for processing friend requests across multiple game server regions with automatic token rotation and real-time statistics.*

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- ⚡ **Parallel Processing** - Execute up to 100 simultaneous requests
- 🔄 **Token Rotation** - Automatic failover mechanisms
- 🌍 **Multi-Region Support** - 18+ server regions
- 📊 **Real-time Stats** - Success/failure tracking
- 🎨 **Modern UI** - Beautiful dark-themed interface

</td>
<td width="50%">

### 🛡️ Technical Features
- 🧵 Multi-threaded architecture
- 🔐 AES encryption for API calls
- 📡 RESTful API endpoints
- 🎭 Dynamic client URL routing
- 📱 Responsive design (80% zoom optimized)

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
Python 3.10+
pip (Python package manager)

# Optional
Docker (for containerized deployment)
```

### Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/spam-pk.git
cd spam-pk
```

2️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

3️⃣ **Configure token files**
```bash
# Create token files for each server region
# Example: token_pk.json, token_ind.json, etc.
```

4️⃣ **Run the application**
```bash
python app.py
```

5️⃣ **Access the interface**
```
Open browser: http://localhost:5000
```

### 🐳 Docker Deployment

```bash
# Build image
docker build -t tsun-spam-api .

# Run container
docker run -p 5000:5000 tsun-spam-api
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoint: Send Friend Request

<table>
<tr>
<td><strong>Method</strong></td>
<td><code>GET</code></td>
</tr>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>/send_request-dev</code></td>
</tr>
<tr>
<td><strong>Description</strong></td>
<td>Sends friend requests to a target player using multiple authentication tokens in parallel</td>
</tr>
</table>

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uid` | string | ✅ Yes | Target player's unique identifier |
| `server` | string | ✅ Yes | Server region code (PK, IND, BR, US, etc.) |

#### Example Request

```bash
curl "http://localhost:5000/send_request-dev?uid=2513698016&server=PK"
```

#### Success Response

```json
{
  "PlayerName": "PlayerUsername",
  "UID": 2513698016,
  "Server": "PK",
  "Success": 87,
  "Failed": 13,
  "Status": 1
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `PlayerName` | string | Target player's display name |
| `UID` | integer | Confirmed player UID |
| `Server` | string | Server region code |
| `Success` | integer | Number of successful requests |
| `Failed` | integer | Number of failed requests |
| `Status` | integer | 1 = Success, 2 = All failed |

#### Error Responses

```json
// Missing UID
{"error": "uid required"}

// Missing Server
{"error": "server required"}

// Token file not found
{"error": "Token file not found for server: PK"}
```

---

## 🌍 Server Regions

### Available Regions

<table>
<tr>
<td align="center">🇵🇰<br><b>PK</b><br>Pakistan</td>
<td align="center">🇮🇳<br><b>IND</b><br>India</td>
<td align="center">🇧🇷<br><b>BR</b><br>Brazil</td>
<td align="center">🇺🇸<br><b>US</b><br>United States</td>
</tr>
<tr>
<td align="center">🌎<br><b>NA</b><br>North America</td>
<td align="center">🌎<br><b>SAC</b><br>South/Central America</td>
<td align="center">🇪🇺<br><b>EU</b><br>Europe</td>
<td align="center">🌍<br><b>ME</b><br>Middle East</td>
</tr>
<tr>
<td align="center">🌍<br><b>AFR</b><br>Africa</td>
<td align="center">🇷🇺<br><b>RU</b><br>Russia</td>
<td align="center">🇮🇩<br><b>ID</b><br>Indonesia</td>
<td align="center">🇹🇭<br><b>TH</b><br>Thailand</td>
</tr>
<tr>
<td align="center">🇻🇳<br><b>VN</b><br>Vietnam</td>
<td align="center">🇸🇬<br><b>SG</b><br>Singapore</td>
<td align="center">🇲🇾<br><b>MY</b><br>Malaysia</td>
<td align="center">🇵🇭<br><b>PH</b><br>Philippines</td>
</tr>
<tr>
<td align="center">🇧🇩<br><b>BD</b><br>Bangladesh</td>
<td align="center" colspan="3">🌐<br><b>Other</b><br>Other Regions</td>
</tr>
</table>

### Client URL Mapping

| Server Regions | Client URL |
|----------------|------------|
| **IND** | `https://client.ind.freefiremobile.com` |
| **BR, US, SAC, NA** | `https://client.us.freefiremobile.com` |
| **EU, ME, ID, TH, VN, SG, BD, PK, MY, PH, RU, AFR, Other** | `https://clientbp.ggblueshark.com` |

---

## ⚙️ Configuration

### Token Files

Create JSON files for each server region with the following format:

```json
[
  {
    "token": "your_auth_token_here_1"
  },
  {
    "token": "your_auth_token_here_2"
  },
  {
    "token": "your_auth_token_here_3"
  }
]
```

**Required Files:**
- `token_pk.json` - Pakistan tokens
- `token_ind.json` - India tokens
- `token_br.json` - Brazil tokens
- `token_us.json` - United States tokens
- *(Create additional files as needed for other regions)*

### Environment Variables

```bash
# Optional: Set custom port
export PORT=5000

# Optional: Enable debug mode
export FLASK_DEBUG=1
```

---

## 🛠️ Tech Stack

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

- **Vanilla JavaScript** - ES6+ features
- **Custom CSS** - Dark theme with gradient accents
- **Responsive Design** - Mobile-optimized (80% zoom)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)

- **Flask 2.0+** - Lightweight web framework
- **Threading** - Parallel request processing
- **Protobuf** - Binary serialization
- **PyCryptodome** - AES encryption

### Dependencies

```
Flask>=2.0.0
requests>=2.25.0
protobuf>=3.19.0
pycryptodome>=3.15.0
urllib3>=1.26.0
```

---

## 📁 Project Structure

```
spam-pk/
├── 📄 app.py                 # Main Flask application
├── 📄 byte.py                # Encryption utilities
├── 📄 dev_generator_pb2.py   # Protobuf definitions
├── 📄 devxt_count_pb2.py     # Protobuf definitions
├── 📄 requirements.txt       # Python dependencies
├── 📄 Dockerfile            # Docker configuration
├── 📄 vercel.json           # Vercel deployment config
├── 📁 static/               # Frontend assets
│   ├── 📄 index.html        # Main HTML page
│   ├── 📄 styles.css        # Stylesheet
│   ├── 📄 main.js           # JavaScript logic
│   └── 🖼️ favicon.png       # Favicon
└── 📁 token files/          # Authentication tokens
    ├── 📄 token_pk.json
    ├── 📄 token_ind.json
    └── ...
```

---

## 🎨 UI Features

### Modern Interface
- 🌑 **Dark Theme** - Easy on the eyes
- 🎯 **Grid Selection** - Visual server picker (4x4 grid on desktop, 2x2 on mobile)
- 📊 **Card-based Results** - Beautiful response display with player info and stats
- 🔄 **Collapsible JSON** - Toggle raw response view
- ⚡ **Optimized Performance** - Smooth on low-end devices

### Design Highlights
- Custom gradient backgrounds
- Smooth transitions
- Responsive layout
- 80% default zoom for better readability
- Icon-based navigation

---

## 🔒 Security Notes

> ⚠️ **Important:** This tool is for educational purposes only. Always respect game terms of service and user privacy.

- Tokens are stored locally in JSON files
- API calls use AES encryption
- No data is logged or stored permanently
- SSL verification can be disabled (use with caution)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**TSun Development Team**

- 🌐 Website: [Your Website]
- 📧 Email: [your.email@example.com]
- 💼 GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Protobuf for efficient data serialization
- All contributors and testers

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ by TSun Development Team**

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/spam-pk?style=social)](https://github.com/yourusername/spam-pk/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/spam-pk?style=social)](https://github.com/yourusername/spam-pk/network/members)

</div>
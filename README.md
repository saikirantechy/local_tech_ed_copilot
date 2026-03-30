<div align="center">
  <!-- Optional Banner -->
  <img src="https://via.placeholder.com/800x200/000000/FFFFFF/?text=Local+Tech-Ed+RAG+Copilot" alt="Project Banner">

  <h1>🤖 Local Tech-Ed RAG Copilot</h1>
  <p><em>A completely local Retrieval-Augmented Generation system. No paid APIs! Running entirely on CPU.</em></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/github/license/YOUR_USERNAME/local_tech_ed_copilot?style=flat-square&color=blue" alt="License">
    <img src="https://img.shields.io/github/stars/YOUR_USERNAME/local_tech_ed_copilot?style=flat-square&color=yellow" alt="Stars">
    <img src="https://img.shields.io/github/forks/YOUR_USERNAME/local_tech_ed_copilot?style=flat-square&color=orange" alt="Forks">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="Contributions welcome">
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python&logoColor=white" alt="Python Version">
  </p>
</div>

---

## 📌 About the Project

**Local Tech-Ed RAG Copilot** is a privacy-first, fully standalone offline learning assistant. Built to run easily on consumer CPUs, it processes documents (PDFs, Markdown, TXT) and builds a searchable index using FAISS, completely avoiding cloud dependencies or expensive API calls. It combines the power of lightweight sentence transformers with the `Qwen2.5-1.5B-Instruct` LLM to give you high-quality, localized answers sourced directly from your materials.

## ✨ Features

- **🔒 100% Local & Private:** No data leaves your machine. No OpenAI API keys required.
- **📄 Multi-Format Support:** Easily ingest `.pdf`, `.md`, and `.txt` documents.
- **⚡ CPU Optimized:** Designed to run efficiently on standard consumer hardware.
- **💬 Interactive Chat UI:** Built with Streamlit for a seamless, modern chatting experience.
- **📚 Accurate Citations:** Transparently shows accurate citations and chunks used to generate answers.

## 🛠️ Tech Stack

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/HuggingFace-F9AB00?style=for-the-badge&logo=HuggingFace&logoColor=white" alt="HuggingFace">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/FAISS-0052CC?style=for-the-badge&logo=Meta&logoColor=white" alt="FAISS">
</div>

## 📸 Screenshots / Demo

_(Replace the placeholder below with an actual screenshot or GIF of your application)_

<div align="center">
  <img src="https://via.placeholder.com/800x450/1A1A1A/FFFFFF/?text=Your+App+Screenshot+Here" alt="Screenshot" width="100%">
</div>

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/local_tech_ed_copilot.git
   cd local_tech_ed_copilot
   ```

2. **Set up a virtual environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Start the Streamlit UI with a single command:

```bash
streamlit run app.py
```

It will automatically launch a local web server (typically at `http://localhost:8501`). Wait a moment for the documents to be chunked, embedded, and indexed locally.

> **Note:** The first time you launch the application, it will securely download the `Qwen2.5-1.5B-Instruct` model and `all-MiniLM-L6-v2` embeddings (~3.5GB total). Ensure you have a stable internet connection. After this one-time download, the Copilot functions **completely offline**.

## 📂 Project Structure

```text
local_tech_ed_copilot/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author & Connect With Me

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/saikirantechy)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/saikirantechy)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/saikirantechy)

---

## 🚀 Community & Platforms

[![WhatsApp Community](https://img.shields.io/badge/WhatsApp%20Community-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://chat.whatsapp.com/Jxo5Ny382rmAT5DEkpmwYy)
[![WhatsApp Channel](https://img.shields.io/badge/WhatsApp%20Channel-128C7E?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029VaesC2lBadmViwYTnj2d)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/saikirantechy)
[![Arattai](https://img.shields.io/badge/Arattai-000000?style=for-the-badge&logo=chat&logoColor=white)](https://aratt.ai/@saikirantechy)

---

## 🎯 SKT Nexus

[![SKT Nexus LinkedIn](https://img.shields.io/badge/SKT%20Nexus-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/skt_nexus)
[![Admin LinkedIn](https://img.shields.io/badge/Admin%20Profile-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saikirantech)

---

<div align="center">
  <b>If you found this project helpful, please don't forget to Star ⭐ this repo!</b>
</div>

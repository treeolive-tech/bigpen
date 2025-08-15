# 🧱 Djanx Base Project

Welcome! This is the official base repository for Djanx-based projects. It's designed to be forked and customized **without modifying the `main` branch**.

---

## 🛠️ How to Customize This Project

If you've already forked this repository, follow these steps to personalize your version:

1. Create a `.dashboard` folder in the root of your fork.  
   Add your own `README.md` inside `.dashboard`.

2. To customize the admin:  
   Create a `dashboard/` folder inside the `admin/` directory and add your code there.

3. To customize the web frontend:  
   Create a `dashboard/` folder inside the `web/app/` directory for your web frontend changes.

---

This setup allows you to:

- Keep your custom code and documentation separate
- Safely pull updates from this base project
- Maintain a clear structure between base and custom logic

📄 [See `.dashboard/README.md`](./.dashboard/README.md) for your custom project documentation.

> 💡 Use the `.dashboard`, `frontend/app/dashboard`, and `admin/dashboard` folders to add your own code without rewriting the upstream files.

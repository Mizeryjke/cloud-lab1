# Звіт про навантажувальне тестування (k6)

## 1. Команда запуску
```bash
k6 run -e TARGET_URL=http://<DNS_ВАШОГО_ALB> loadtest/script.js
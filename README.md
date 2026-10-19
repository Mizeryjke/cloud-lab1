# Лабораторна робота №1 з хмарних технологій

## Опис проєкту
REST API на FastAPI для роботи з базою даних PostgreSQL, запакований у Docker-контейнер та розгорнутий в AWS з використанням Infrastructure as Code (Terraform) і CI/CD через GitHub Actions.

**Публічна адреса (Swagger UI):**  
http://cloud-lab1-alb-1417131122.eu-north-1.elb.amazonaws.com/docs


## Структура проєкту
cloud-lab1/
├── app/
│   ├── main.py          # Код REST API (FastAPI + SQLAlchemy)
│   └── requirements.txt # Залежності Python
├── terraform/           # Опис інфраструктури AWS (VPC, ECR, RDS, ALB, ECS)
├── .github/workflows/
│   └── deploy.yml       # GitHub Actions Workflow (CI/CD)
├── Dockerfile           # Фіксований базовий образ, non-root user
├── compose.yaml         # Локальне середовище (API + Postgres з volume)
└── README.md            # Документація проєкту
# Лабораторна робота №1 з хмарних технологій

## Опис проєкту
REST API на FastAPI для роботи з базою даних PostgreSQL, запакований у Docker-контейнер та розгорнутий в AWS з використанням Infrastructure as Code (Terraform) і CI/CD через GitHub Actions.

**Публічна адреса (Swagger UI):**  
http://cloud-lab1-alb-1417131122.eu-north-1.elb.amazonaws.com/docs


## Структура проєкту
cloud-lab1/

```text
cloud-lab1/
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions Workflow (CI/CD)
├── app/
│   ├── main.py              # Код REST API (FastAPI + SQLAlchemy)
│   └── requirements.txt     # Залежності Python
├── terraform/               # Опис інфраструктури AWS (VPC, ECR, RDS, ALB, ECS)
│   ├── main.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── .gitignore               # Ігнорування секретів та тимчасових файлів
├── compose.yaml             # Локальне середовище (API + Postgres з volume)
├── Dockerfile               # Фіксований базовий образ, non-root user
└── README.md                # Документація проєкту
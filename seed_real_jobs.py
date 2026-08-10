import sys
import os
import uuid

# add backend path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.core.database import SessionLocal
from app.models.job import Job
from app.models.company import Company
from app.models.application import Application

def seed_database():
    db = SessionLocal()
    try:
        print("Cleaning up old database entries...")
        # Clear out existing applications, jobs, and companies to avoid UUID conflicts
        db.query(Application).delete()
        db.query(Job).delete()
        db.query(Company).delete()
        db.commit()
        print("Cleanup successful.")

        # Seed Companies
        companies_data = [
            {
                "id": uuid.uuid4(),
                "name": "Google",
                "description": "Google's mission is to organize the world's information and make it universally accessible and useful.",
                "website": "https://google.com",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"
            },
            {
                "id": uuid.uuid4(),
                "name": "Meta",
                "description": "Meta builds technologies that help people connect, find communities, and grow businesses.",
                "website": "https://meta.com",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg"
            },
            {
                "id": uuid.uuid4(),
                "name": "Amazon",
                "description": "Amazon is guided by four principles: customer obsession rather than competitor focus, passion for invention, commitment to operational excellence, and long-term thinking.",
                "website": "https://amazon.com",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"
            },
            {
                "id": uuid.uuid4(),
                "name": "Stripe",
                "description": "Stripe is a financial infrastructure platform for the internet. Millions of companies use Stripe to accept payments, grow their revenue, and accelerate new business opportunities.",
                "website": "https://stripe.com",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg"
            },
            {
                "id": uuid.uuid4(),
                "name": "Netflix",
                "description": "Netflix is one of the world's leading entertainment services with over 230 million paid memberships in over 190 countries.",
                "website": "https://netflix.com",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"
            }
        ]

        companies = []
        for c_data in companies_data:
            comp = Company(**c_data)
            db.add(comp)
            companies.append(comp)
        db.commit()
        print(f"Seeded {len(companies)} companies.")

        # Map companies list by name for easy job linking
        companies_map = {c.name: c for c in companies}

        # Seed Jobs
        jobs_data = [
            {
                "title": "Software Engineer, Frontend",
                "description": "Join our Search frontend team to build responsive, fast, and accessible user interfaces. Requires proficiency in React, JavaScript, HTML5, CSS3, and optimizing web performance. Experience with Next.js or Vite is highly valued.",
                "company_id": companies_map["Google"].id,
                "location": "Mountain View, CA (Hybrid)",
                "salary_min": 1200000.0,
                "salary_max": 2000000.0
            },
            {
                "title": "Staff Full-Stack Developer",
                "description": "Develop high-converting checkout forms and payment processing components. Requires mastery of React, JavaScript, Node.js, and RESTful APIs. Experience with CockroachDB, PostgreSQL, and building fintech infrastructure is preferred.",
                "company_id": companies_map["Stripe"].id,
                "location": "Bengaluru, India",
                "salary_min": 1800000.0,
                "salary_max": 3000000.0
            },
            {
                "title": "Senior Backend Architect",
                "description": "Build high-performance distributed systems. Master Python, FastAPI, Docker, and PostgreSQL. Implement real-time streaming architectures and integrate robust security modules. Experience with CockroachDB pgvector is a big plus.",
                "company_id": companies_map["Meta"].id,
                "location": "Remote (India)",
                "salary_min": 2500000.0,
                "salary_max": 3500000.0
            },
            {
                "title": "Cloud Solutions & Systems Engineer",
                "description": "Design reliable, fault-tolerant cloud environments. Deploy infrastructure using Terraform, AWS services (EC2, ECS, Bedrock, S3), and Kubernetes. Set up continuous integration and delivery pipelines.",
                "company_id": companies_map["Amazon"].id,
                "location": "Seattle, WA (Remote)",
                "salary_min": 1500000.0,
                "salary_max": 2600000.0
            },
            {
                "title": "Machine Learning Platform Engineer",
                "description": "Build infrastructure to serve massive recommendation algorithms. Proficiency with Python, TensorFlow/PyTorch, Docker, Kubernetes, and GPU orchestration. Help Netflix personalize experiences for millions of users worldwide.",
                "company_id": companies_map["Netflix"].id,
                "location": "Los Gatos, CA (Hybrid)",
                "salary_min": 2800000.0,
                "salary_max": 4200000.0
            },
            {
                "title": "React Frontend Specialist",
                "description": "Build and style elegant client-facing interfaces. Work closely with product design to translate Figma mockups into reusable React components. Leverage CSS modules, Tailwind CSS, and state management via Zustand.",
                "company_id": companies_map["Google"].id,
                "location": "Bengaluru, India (Hybrid)",
                "salary_min": 900000.0,
                "salary_max": 1600000.0
            },
            {
                "title": "Junior Python Developer",
                "description": "Excellent entry role for a passionate backend coder. Work with Python, Flask, FastAPI, and PostgreSQL. Support senior engineers in building payment processors and reporting pipelines.",
                "company_id": companies_map["Stripe"].id,
                "location": "Remote (India)",
                "salary_min": 600000.0,
                "salary_max": 1000000.0
            }
        ]

        for j_data in jobs_data:
            job = Job(**j_data)
            db.add(job)
        db.commit()
        print(f"Seeded {len(jobs_data)} realistic jobs.")

    except Exception as e:
        print("Seeding failed:")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

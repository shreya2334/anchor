import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base

import app.models.user
import app.models.roadmap
import app.models.user_roadmap

from app.models.roadmap import Roadmap, Step


Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Roadmap).count() > 0:
    print('Already seeded.')
    db.close()
    exit()


roadmaps = [
    {
        'title': 'Frontend Web Development',
        'description': 'Go from zero to building real React apps.',
        'category': 'Web Dev',
        'difficulty': 'beginner',
        'estimated_hours': 80,
        'tags': 'html,css,javascript,react',

        'steps': [
            (
                'HTML Fundamentals',
                'Learn document structure and semantic tags.',
                'https://www.youtube.com/watch?v=qz0aGYrrlhU',
                'youtube',
                1,
                120
            ),

            (
                'CSS Styling',
                'Master layouts, flexbox and grid.',
                'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
                'youtube',
                2,
                150
            ),

            (
                'JavaScript Basics',
                'Variables, functions, DOM manipulation.',
                'https://javascript.info',
                'article',
                3,
                180
            ),

            (
                'React Fundamentals',
                'Components, props, state and hooks.',
                'https://react.dev/learn',
                'docs',
                4,
                200
            ),

            (
                'Build a Portfolio Project',
                'Apply everything you learned.',
                'https://www.youtube.com/watch?v=xV7S8BhIeBo',
                'youtube',
                5,
                240
            ),
        ]
    },

    {
        'title': 'Python for Data Science',
        'description': 'Learn Python then apply it to real data problems.',
        'category': 'Data Science',
        'difficulty': 'beginner',
        'estimated_hours': 60,
        'tags': 'python,pandas,numpy,visualization',

        'steps': [
            (
                'Python Basics',
                'Syntax, data types, control flow.',
                'https://www.youtube.com/watch?v=rfscVS0vtbw',
                'youtube',
                1,
                120
            ),

            (
                'NumPy & Pandas',
                'Arrays, dataframes, data cleaning.',
                'https://pandas.pydata.org/docs/getting_started',
                'docs',
                2,
                150
            ),

            (
                'Data Visualization',
                'Matplotlib and Seaborn charts.',
                'https://www.youtube.com/watch?v=a9UrKTVEeZA',
                'youtube',
                3,
                120
            ),

            (
                'Exploratory Data Analysis',
                'Real-world dataset walkthrough.',
                'https://www.kaggle.com/learn/pandas',
                'course',
                4,
                180
            ),
        ]
    },

    {
        'title': 'Full-Stack with Next.js',
        'description': 'Build production-ready full-stack apps.',
        'category': 'Web Dev',
        'difficulty': 'intermediate',
        'estimated_hours': 100,
        'tags': 'nextjs,typescript,api,database',

        'steps': [
            (
                'Next.js App Router',
                'Pages, layouts, routing.',
                'https://nextjs.org/docs',
                'docs',
                1,
                120
            ),

            (
                'TypeScript Essentials',
                'Types, interfaces, generics.',
                'https://www.typescriptlang.org/docs/handbook/intro.html',
                'docs',
                2,
                120
            ),

            (
                'API Routes & Server Actions',
                'Backend logic in Next.js.',
                'https://www.youtube.com/watch?v=wm5gMKuwSYk',
                'youtube',
                3,
                150
            ),

            (
                'PostgreSQL & Prisma',
                'Database design and ORM.',
                'https://www.prisma.io/learn',
                'course',
                4,
                180
            ),

            (
                'Deploy to Vercel',
                'CI/CD and production best practices.',
                'https://vercel.com/docs',
                'docs',
                5,
                60
            ),
        ]
    },

    {
        'title': 'SQL for Data Analytics',
        'description': 'Master SQL queries and real-world analytics workflows.',
        'category': 'Data Science',
        'difficulty': 'beginner',
        'estimated_hours': 40,
        'tags': 'sql,analytics,database,queries',

        'steps': [
            (
                'SQL Fundamentals',
                'Learn SELECT, WHERE, ORDER BY.',
                'https://www.w3schools.com/sql/',
                'docs',
                1,
                90
            ),

            (
                'Filtering & Aggregations',
                'COUNT, SUM, AVG, GROUP BY.',
                'https://mode.com/sql-tutorial/',
                'course',
                2,
                120
            ),

            (
                'SQL Joins',
                'Master INNER, LEFT and RIGHT joins.',
                'https://www.youtube.com/watch?v=9Pzj7Aj25lw',
                'youtube',
                3,
                120
            ),

            (
                'Window Functions',
                'Ranking and analytical queries.',
                'https://mode.com/sql-tutorial/sql-window-functions/',
                'article',
                4,
                150
            ),

            (
                'Analytics Case Study',
                'Solve a real business problem using SQL.',
                'https://www.kaggle.com/',
                'project',
                5,
                180
            ),
        ]
    },

    {
        'title': 'Machine Learning Fundamentals',
        'description': 'Build and evaluate machine learning models from scratch.',
        'category': 'AI/ML',
        'difficulty': 'intermediate',
        'estimated_hours': 70,
        'tags': 'machinelearning,scikit-learn,python',

        'steps': [
            (
                'ML Foundations',
                'Understand supervised and unsupervised learning.',
                'https://developers.google.com/machine-learning/crash-course',
                'course',
                1,
                120
            ),

            (
                'Regression Models',
                'Linear regression and evaluation metrics.',
                'https://scikit-learn.org/stable/',
                'docs',
                2,
                150
            ),

            (
                'Classification Models',
                'Decision trees and logistic regression.',
                'https://www.youtube.com/watch?v=7eh4d6sabA0',
                'youtube',
                3,
                180
            ),

            (
                'Model Evaluation',
                'Confusion matrix, precision, recall.',
                'https://developers.google.com/machine-learning/crash-course/classification',
                'article',
                4,
                120
            ),

            (
                'End-to-End ML Project',
                'Train and deploy a model.',
                'https://www.kaggle.com/learn/intro-to-machine-learning',
                'course',
                5,
                240
            ),
        ]
    },

    {
        'title': 'Deep Learning with TensorFlow',
        'description': 'Build neural networks and computer vision models.',
        'category': 'AI/ML',
        'difficulty': 'advanced',
        'estimated_hours': 90,
        'tags': 'tensorflow,keras,deeplearning',

        'steps': [
            (
                'Neural Network Basics',
                'Understand neurons and layers.',
                'https://www.youtube.com/watch?v=aircAruvnKk',
                'youtube',
                1,
                120
            ),

            (
                'TensorFlow Essentials',
                'Build your first neural network.',
                'https://www.tensorflow.org/tutorials',
                'docs',
                2,
                150
            ),

            (
                'Computer Vision',
                'Image classification using CNNs.',
                'https://www.tensorflow.org/tutorials/images/classification',
                'course',
                3,
                180
            ),

            (
                'Model Optimization',
                'Improve performance and accuracy.',
                'https://keras.io/guides/',
                'docs',
                4,
                120
            ),

            (
                'Capstone Project',
                'Build a deep learning application.',
                'https://www.kaggle.com/',
                'project',
                5,
                240
            ),
        ]
    },

    {
        'title': 'Data Analyst Career Path',
        'description': 'Learn the essential skills required for modern data analysts.',
        'category': 'Analytics',
        'difficulty': 'beginner',
        'estimated_hours': 60,
        'tags': 'analytics,excel,sql,powerbi',

        'steps': [
            (
                'Excel Fundamentals',
                'Learn formulas, pivots and dashboards.',
                'https://www.youtube.com/watch?v=Vl0H-qTclOg',
                'youtube',
                1,
                120
            ),

            (
                'SQL for Analysts',
                'Extract insights from databases.',
                'https://mode.com/sql-tutorial/',
                'course',
                2,
                150
            ),

            (
                'Power BI Basics',
                'Build interactive dashboards.',
                'https://learn.microsoft.com/en-us/training/powerplatform/power-bi/',
                'course',
                3,
                150
            ),

            (
                'Business Analytics',
                'Turn data into decisions.',
                'https://www.coursera.org/',
                'course',
                4,
                120
            ),

            (
                'Capstone Case Study',
                'Analyze a business dataset and present actionable insights.',
                'https://www.kaggle.com/datasets/vivek468/superstore-dataset-final',
                'course',
                5,
                180
            ),
        ]
    },
]


for rm_data in roadmaps:

    steps_data = rm_data.pop('steps')

    rm = Roadmap(**rm_data)

    db.add(rm)

    db.flush()

    for s in steps_data:
        db.add(
            Step(
                roadmap_id=rm.id,
                title=s[0],
                description=s[1],
                resource_url=s[2],
                resource_type=s[3],
                order=s[4],
                duration_minutes=s[5]
            )
        )

db.commit()

print(f'Seeded {len(roadmaps)} roadmaps successfully!')

db.close()
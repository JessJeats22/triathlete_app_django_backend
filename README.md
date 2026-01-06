# Triathlon Trails API — Django REST Backend

As a keen Triathlete myself, I created a full-stack training route planner for endurance athletes (TriTrails)
The app provides endpoints for trails, GPX-derived route metrics, favourites, weather data, and map-based Points of Interest (POIs), with secure authentication and owner-based permissions.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Related Repositories & Deployment](#related-repositories--deployment)
- [Features At a Glance](#features-at-a-glance)
- [Architecture & Data Model](#architecture--data-model)
  - [Users](#users)
  - [Trails](#trails)
  - [Points of Interest POIs](#points-of-interest-pois)
- [Authentication](#authentication)
- [GPX Processing & Derived Metrics](#gpx-processing--derived-metrics)
- [Weather Integration](#weather-integration)
- [API Endpoints](#api-endpoints)
  - [Auth](#auth)
  - [Users & Profile](#users--profile)
  - [Trails](#trails-1)
  - [Favourites](#favourites)
  - [Trail Images](#trail-images)
  - [Trail Weather](#trail-weather)
  - [Points of Interest](#points-of-interest)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [Design Decisions & Trade-Offs](#design-decisions--trade-offs)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [Project Context](#project-context)

---

## Overview

The Triathlon Trails API is built with **Django REST Framework** and serves as the backend for a React single-page application.

The API supports:

- Managing **trails** (swim, bike, run)
- Parsing **GPX files** to compute distance, elevation gain, and starting coordinates
- Creating and displaying **map-based POIs**
- **JWT authentication** with user profiles and favourites
- Trail-specific **live weather data** via OpenWeather

The project models realistic full-stack architecture, separation of concerns, and production-style API patterns.

---

## Related Repositories & Deployment

**Frontend (React SPA)**  
https://github.com/JessJeats22/triathlete_app_react_frontend

**Live Frontend App**  
https://triathleteappreactfrontend.netlify.app/trails

---

## Features At a Glance

- Django REST API with **JWT authentication**
- Custom `User` model with profile image + favourites
- GPX-backed **distance and elevation** computation
- Leaflet-ready **lat/lon coordinates**
- Trail ownership and **role-aware permissions**
- Trail weather endpoint (OpenWeather)
- Points of Interest (lat/lon, description, owner)
- Clean separation of:
  - models
  - serializers
  - services
  - permissions
  - views

---


## Technical Highlights

- **Service-based GPX parser** computes distance, elevation gain, and start coordinates using `gpxpy` + Haversine distance.
- **Owner-restricted resources** via custom `IsOwnerOrReadOnly` permission class.
- **Derived trail metrics** are computed server-side after upload to ensure consistent, trustworthy data.
- **Favourites system** implemented as a Many-to-Many relation with optimistic UI patterns on the frontend.
- **Backend-proxied weather integration** prevents API key exposure and standardises responses.
- **Context-aware serializers** (e.g., `is_favourited`) adapt output based on authentication.
- **Populated serializers** used for nested representations without over-fetching.
- **Consistent async and error-handling patterns** across endpoints.

---

## Architecture & Data Model

### Users

Custom user model extending `AbstractUser`, including:

- `email` (unique)
- `profile_image`
- `favourited_trails` — Many-to-Many relationship with trails
- reverse relation for owned trails: `trails_owned`

`/auth/me/` returns:

- profile information
- created trails
- favourited trails

---

### Trails

A trail represents a training route and includes:

- Type (`swim | bike | run`)
- Location (`country`, `city_town`)
- Coordinates (optional lat/lon — also derived from GPX)
- Description
- Images (`ArrayField` of URLs)
- Cloudinary-hosted `gpx_url`
- Owner (`created_by`)

GPX files are parsed to compute:

- `distance_km`
- `elevation_gain`
- first track point latitude / longitude

Ownership governs update/delete behaviour.

---

### Points of Interest (POIs)

POIs are spatial markers attached to trails:

- Name + description
- Latitude / longitude
- Owned by the creating user
- Related to a specific trail

Only the **trail owner** may add POIs.

---

## Authentication

Authentication uses **djangorestframework-simplejwt** with custom claims:

- tokens include basic user details
- frontend can hydrate user state without an extra fetch
- `/auth/sign-up/` handles password validation + hashing
- `/auth/me/` returns current user with related trail data

Authenticated requests require:

Authorization: Bearer <token>

---

## GPX Processing & Derived Metrics

GPX files are fetched from Cloudinary and parsed using **gpxpy**.

The backend computes the following values:

- **Total distance** (via the Haversine formula between GPS points)
- **Cumulative positive** elevation gain
- **Starting latitude and longitude**

These metrics are written back to the Trail record after creation to ensure consistent and trustworthy route data.

## Weather Integration

Each trail exposes a dedicated weather endpoint: GET /trails/<id>/weather/


This endpoint returns:

- **Current temperature**
- **Feels-like temperature**
- **Wind speed**
- **Short-term forecast (~24 hours)**

All requests are proxied through the backend in order to:

- **Protect API keys**
- **Provide a consistent and frontend-friendly response shape**

## API Endpoints

> Base paths reflect app-level routing (`/trails/`, `/auth/`, `/poi/`).

---

### Auth

- `POST /auth/sign-up/`
- `POST /auth/sign-in/`
- `GET /auth/me/`

---

### Users & Profile

GET /auth/me/


Returns the authenticated user profile, including:

- created trails
- favourited trails

---

### Trails

- `GET /trails/` — list all trails  
- `POST /trails/` — create a trail (owner = authenticated user)  
- `GET /trails/<id>/` — retrieve a populated trail (owner + POIs)  
- `PUT /trails/<id>/` — update a trail (owner only)  
- `PATCH /trails/<id>/` — partial update (owner only)  
- `DELETE /trails/<id>/` — delete a trail (owner only)  

When authenticated, responses also include:

- `is_favourited` — indicates whether the trail has been favourited by the current user

### Favourites

- `POST /trails/<id>/favourite/`
- `DELETE /trails/<id>/favourite/`

These endpoints add or remove a trail from `User.favourited_trails`.

---

### Trail Images

DELETE /trails/<id>/images/


Request body:
{
"image_url": "<url>"
}

Removes a specific image from the trail’s `images` gallery.

---

### Trail Weather

GET /trails/<id>/weather/


Returns combined **current conditions** and **short-term forecast** for the trail location.

---

### Points of Interest (POIs)

- `GET /poi/trails/<trail_id>/pois/`
- `POST /poi/trails/<trail_id>/pois/` — **owner-only**
- `GET /poi/<id>/`
- `PUT /poi/<id>/`
- `PATCH /poi/<id>/`
- `DELETE /poi/<id>/`

Modification of POIs is restricted to the **creating user** (`IsOwnerOrReadOnly`).


## Getting Started

### Prerequisites

- Python **3.10+**
- `pip` / `virtualenv`
- PostgreSQL (or SQLite for local development)
- OpenWeather API key

---

### Installation

```bash
git clone https://github.com/JessJeats22/triathlete_app_django_backend.git
cd triathlete_app_django_backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Environment Variables

Typical configuration includes:
- SECRET_KEY
- DEBUG
- database config or DATABASE_URL
- OPENWEATHER_API_KEY
- CORS origin settings for the frontend


## Running the Server

```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

---

## Technologies Used

**Backend**

- Python • Django • Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt (JWT authentication)
- gpxpy (GPX parsing)
- Requests (HTTP client)

**External Services**

- OpenWeather API (trail-specific weather data)
- Cloudinary (image + GPX file storage)

**Development & Tooling**

- Git / GitHub
- VS Code
- Virtualenv

---

## Project Brief

This backend was built as part of the **General Assembly Software Engineering Immersive** program.

The brief required:

- A Django REST API with relational data models
- A separate React frontend consuming the API
- Full CRUD functionality with authentication and permissions
- Public deployment of both applications
- Clean, maintainable and professionally structured code

The project emphasised **API design, data modelling, and realistic feature implementation** over simple CRUD-only behaviour.

---

## Planning

Key planning activities included:

- Designing an ERD for Users → Trails → POIs → Favourites
- Defining API routes and expected response shapes
- Prioritising MVP features before enhancements
- Sequencing backend implementation to unblock frontend development

Early attention was given to **data relationships and permissions**, reducing the need for major refactors later in the sprint.

---

## Build / Code Process

The backend was developed iteratively:

1. Implemented the custom user model and JWT authentication
2. Built the Trail model and GPX metrics service
3. Added favourites and ownership-based permissions
4. Introduced Points of Interest tied to trails
5. Integrated backend-proxied weather requests
6. Refined serializers and nested representations

Where trade-offs were required, **clarity, correctness, and maintainability** were prioritised.

---

## Challenges

- Learning DRF conventions while delivering within a 7-day sprint
- Handling derived data from GPX files safely and accurately
- Designing permissions that balanced UX simplicity with security
- Keeping the codebase consistent as new features were added

---

## Wins

- Delivered genuinely useful behaviour beyond basic CRUD
- Achieved strong separation of concerns with reusable service logic
- Integrated external services securely and cleanly
- Built a scalable foundation for future mapping and training features

---

## Key Learnings

- Greater confidence working with Django ORM and DRF serializers
- Deeper understanding of relational data modelling and API design
- The value of isolating domain logic in service modules
- Importance of aligning backend behaviour with frontend consumption patterns
- Improved debugging and decision-making under time constraints

---

## Design Decisions & Trade-Offs

- `ArrayField` used for images to keep the model lightweight during the sprint
- Metrics derived server-side to guarantee consistent trail data
- Weather calls handled in the backend to avoid exposing API keys
- Permissions kept explicit and restrictive to reduce ambiguity
- Some abstractions intentionally deferred to maintain delivery momentum

---

## Known Limitations

- Limited server-side filtering and search on `/trails/`
- GPX parsing assumes a conventional GPX file structure
- Weather endpoint has minimal failure-mode feedback
- Some upload and error states are logged rather than surfaced in the UI

---

## Future Improvements

- Add API-level filtering and search capabilities
- Extend GPX metrics (min/max elevation, descent, segment stats)
- Allow collaborative or shared POI management
- Add OpenAPI / Swagger documentation
- Improve validation and user-visible error responses

---

## Project Context

- **Timeframe:** 7-day sprint  
- **Role:** Solo developer  
- **Responsibilities:** planning, modelling, API design, implementation, testing, deployment

This backend was designed to demonstrate **professional full-stack engineering practices** with realistic architecture, external integrations, and domain-driven behaviour.

---

# Rewild Frontend

React + Vite frontend for REWILD's guided site wizard and scenario dashboard.

## Requirements
- Node.js 20.19+ (Vite 7 requirement)
- npm

## Setup
```bash
cd frontend
npm install
```

## Run (Development)
```bash
cd frontend
npm run dev
```

The dev server proxies `/api/*` requests to `http://localhost:8000` via `vite.config.js`.

## Build
```bash
cd frontend
npm run build
```

## Validation
```bash
cd frontend
npm run lint
npm run build
```

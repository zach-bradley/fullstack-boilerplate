# Frontend Django Template

This is a Vue.js frontend template designed to work with the Django backend template. It includes authentication, routing, and state management out of the box.

## Features

- Vue 3 with TypeScript
- Ionic Vue UI components
- Pinia state management
- Vue Router with authentication guards
- Axios for API calls
- ESLint and TypeScript configuration

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Setup

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create a `.env.local` file (optional) to override environment variables:
```bash
VUE_APP_API_URL=http://localhost:8000
NODE_ENV=development
```

3. Start the development server:
```bash
npm run serve
# or
yarn serve
```

The application will be available at `http://localhost:8080`

## Project Structure

```
src/
├── assets/         # Static assets
├── components/     # Reusable components
├── router/         # Vue Router configuration
├── services/       # API services
├── store/          # Pinia stores
├── views/          # Page components
├── App.vue         # Root component
└── main.ts         # Application entry point
```

## Available Scripts

- `npm run serve` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Lint and fix files

## API Integration

The frontend is configured to proxy API requests to the Django backend running on `http://localhost:8000`. This can be changed in the `vue.config.js` file.

## Authentication

The template includes:
- User registration
- User login
- Token-based authentication
- Protected routes
- Automatic token refresh

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 
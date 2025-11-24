# TicketBot Frontend

A React-based frontend for the TicketBot application that monitors TicketMaster events for ticket availability.

## Features

- Create subscriptions to TicketMaster events by providing email and event URL
- View all subscriptions in a clean, organized list
- Toggle subscription active/inactive status
- Delete subscriptions
- Real-time updates when managing subscriptions
- Responsive design with Tailwind CSS

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Fetch API** - HTTP requests to backend

## Prerequisites

- Node.js 18+ or npm/yarn/pnpm
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Development Mode

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Production Build

Build for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── subscriptions.js      # API service layer
│   ├── components/
│   │   ├── SubscriptionForm.jsx  # Form to create subscriptions
│   │   └── SubscriptionList.jsx  # List view of subscriptions
│   ├── App.jsx                    # Main app component
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Global styles with Tailwind
├── index.html                     # HTML template
├── vite.config.js                 # Vite configuration
├── tailwind.config.js             # Tailwind configuration
└── package.json
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend.

### Backend Setup

1. Start the backend services:
```bash
cd ..
docker-compose up
```

2. The API will be available at `http://localhost:8000`
3. API documentation: `http://localhost:8000/docs`

## Usage

1. **Create a Subscription**:
   - Enter your email address
   - Paste the full TicketMaster event URL
   - Click "Create Subscription"

2. **Manage Subscriptions**:
   - View all your subscriptions in the list below
   - Click "Pause" to temporarily disable monitoring
   - Click "Activate" to resume monitoring
   - Click "Delete" to remove a subscription

## Configuration

To change the backend API URL, edit `src/api/subscriptions.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Development Notes

- The frontend uses Vite's default port (5173)
- Hot module replacement is enabled in development
- CORS is configured in the backend to allow requests from `localhost:5173`

## Future Enhancements

- User authentication and login
- Display full event details (not just IDs)
- Email notification preferences
- Subscription history and analytics
- Dark mode support
- WebSocket support for real-time ticket availability updates

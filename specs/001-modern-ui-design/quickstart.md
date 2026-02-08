# Quickstart Guide: Modern & Best-in-Class Frontend UI

## Prerequisites

- Node.js v18 or higher
- npm or yarn package manager
- Git for version control
- Better Auth configured with JWT plugin for authentication

## Setup Instructions

### 1. Clone and Navigate
```bash
# Assuming this is part of a monorepo structure
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Copy the environment example and configure your settings:

```bash
cp .env.example .env.local
```

Configure the following variables:
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Your Better Auth API endpoint
- `NEXT_PUBLIC_BETTER_AUTH_TOKEN`: Shared secret for JWT verification
- Any other required environment variables

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

Visit `http://localhost:3000` to see the application.

## Key Technologies & Frameworks

### Next.js 16+ (App Router)
- File-based routing system in `app/` directory
- Server Components by default for better performance
- Client Components when interactivity is needed (`'use client'` directive)

### Tailwind CSS
- Utility-first CSS framework for rapid UI development
- Custom design tokens configured in `tailwind.config.js`
- Dark mode support via `dark:` variant

### React
- Component-based architecture
- Hooks for state and lifecycle management
- Context API for global state (theme, authentication)

## Folder Structure Overview

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/            # Authentication-related routes
│   │   ├── dashboard/         # Protected dashboard routes
│   │   ├── globals.css        # Global styles and Tailwind directives
│   │   ├── layout.tsx         # Root layout with providers
│   │   └── page.tsx           # Home page
│   ├── components/            # Reusable UI components
│   │   ├── ui/               # Atomic UI elements
│   │   ├── auth/             # Authentication-specific components
│   │   ├── tasks/            # Task management components
│   │   └── navigation/       # Navigation components
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                   # Utilities and API functions
│   └── providers/             # React Context providers
├── public/                    # Static assets
├── next.config.js             # Next.js configuration
├── tailwind.config.js         # Tailwind CSS customization
└── package.json               # Project dependencies
```

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run production build locally
npm start

# Run linting
npm run lint

# Run tests
npm run test

# Format code with Prettier
npm run format
```

## Component Development

### Creating New UI Components

1. Place new components in the appropriate subdirectory under `src/components/`
2. Follow the atomic design pattern:
   - Atoms: Basic UI elements (buttons, inputs, etc.)
   - Molecules: Combinations of atoms (input groups, button groups)
   - Organisms: Complex components (cards, forms, navigation)
3. Export components individually and via index.ts files

### Component Guidelines
- Use TypeScript for all components
- Implement proper prop typing
- Follow accessibility best practices (ARIA labels, keyboard navigation)
- Ensure responsive design with Tailwind's responsive prefixes
- Use consistent design tokens (colors, spacing, typography) from the theme

### Example Component Structure
```typescript
// src/components/ui/Button.tsx
'use client'

import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  // Base classes
  'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = ({ className, variant, size, asChild = false, ...props }: ButtonProps) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
```

## API Integration

### Making API Calls
Use the centralized API service in `src/lib/api.ts` for all backend communications:

```typescript
// Example usage in a component
import { apiClient } from '@/lib/api'

const fetchTasks = async () => {
  try {
    const response = await apiClient.get('/tasks')
    return response.data
  } catch (error) {
    console.error('Error fetching tasks:', error)
    throw error
  }
}
```

### Authentication Handling
- All API calls automatically include JWT tokens from auth context
- Unauthorized responses trigger redirect to login
- Refresh token mechanism handles token expiration

## Theming & Styling

### Using Design Tokens
The application follows a consistent design system using Tailwind's configuration:

```typescript
// In components, use Tailwind classes directly
<div className="bg-card text-card-foreground rounded-xl p-6 shadow-lg">
  {/* Component content */}
</div>

// Or for responsive designs
<div className="hidden md:flex space-x-4">
  {/* Desktop-only content */}
</div>
```

### Dark Mode
The application supports both light and dark themes:
- Automatic detection via `prefers-color-scheme`
- Manual toggle through theme context
- All components implement the `dark:` variant appropriately

## Testing

### Running Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Test Structure
Tests follow the same folder structure as the source:
- Unit tests for individual components and utilities
- Integration tests for component combinations
- End-to-end tests for critical user flows

## Deployment

### Production Build
```bash
npm run build
```

The resulting build will be optimized for production with:
- Code splitting
- Asset optimization
- Bundle analysis
- Prerendering (SSR/static generation)

### Environment-Specific Configuration
For different environments, update the environment variables accordingly:
- Development: Local API endpoints
- Staging: Staging API endpoints
- Production: Production API endpoints
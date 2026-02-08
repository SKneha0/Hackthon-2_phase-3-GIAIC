# Data Model: Modern & Best-in-Class Frontend UI

## UI Component Hierarchy

### Atomic Components (Atoms)
- **Button**: Configurable button with variants (primary, secondary, ghost, destructive), sizes (sm, md, lg), loading states, and accessibility props
- **Input**: Text, email, password inputs with validation states, prefixes, suffixes, and helper text
- **Checkbox**: Accessible checkbox with indeterminate states, custom styling, and label integration
- **Card**: Flexible container with configurable padding, borders, shadows, and responsive behavior
- **Skeleton**: Loading placeholders matching dimensions of final content
- **Typography**: Heading, paragraph, and label components with consistent sizing and spacing

### Molecular Components (Molecules)
- **InputWithLabel**: Input field with associated label and optional helper/error text
- **ButtonGroup**: Collection of related buttons with consistent spacing
- **AuthInput**: Input with validation, error display, and icon support for login forms
- **TaskBadge**: Status indicators for due dates, priority, or tags with color coding

### Organism Components (Organisms)
- **AuthForm**: Complete login/signup form with field validation, error handling, and submission states
- **TaskCard**: Individual task display with title, description, due date, completion toggle, and actions
- **TaskForm**: Form for creating/editing tasks with validation and submission handling
- **Navigation**: Sidebar navigation with menu items, logo, and user profile
- **Modal**: Overlay component with header, body, footer, and backdrop dismiss functionality
- **EmptyState**: Illustration with title and description for empty collections

### Template Components (Templates)
- **PageLayout**: Wrapper providing consistent page structure with header, navigation, and main content area
- **DashboardLayout**: Specialized layout for the main dashboard with sidebar and main content
- **AuthLayout**: Centered layout for authentication pages with logo and form container

### Page Components (Pages)
- **LoginPage**: Complete login page with form, links, and branding
- **SignupPage**: Complete signup page with form, terms, and branding
- **DashboardPage**: Main dashboard with task list, filters, and add task functionality

## Design Token System

### Color Palette
- **Neutral Colors**: gray-50 to gray-950 (light theme), gray-50 to gray-950 (dark theme with different emphasis)
- **Primary Colors**: blue-500 (main), blue-600 (hover), blue-400 (light variant)
- **Success Colors**: green-500 (success state)
- **Warning Colors**: amber-500 (warning state)
- **Destructive Colors**: red-500 (error/destructive actions)
- **Accent Colors**: violet-500 (accent elements)

### Typography Scale
- **Heading 1**: 2.5rem (40px) / 2.25rem (36px) for mobile
- **Heading 2**: 2rem (32px) / 1.75rem (28px) for mobile
- **Heading 3**: 1.5rem (24px) / 1.25rem (20px) for mobile
- **Body Large**: 1.125rem (18px)
- **Body Regular**: 1rem (16px)
- **Body Small**: 0.875rem (14px)
- **Caption**: 0.75rem (12px)

### Spacing Scale
- **Space 1**: 0.25rem (4px)
- **Space 2**: 0.5rem (8px)
- **Space 3**: 0.75rem (12px)
- **Space 4**: 1rem (16px)
- **Space 5**: 1.25rem (20px)
- **Space 6**: 1.5rem (24px)
- **Space 8**: 2rem (32px)
- **Space 10**: 2.5rem (40px)
- **Space 12**: 3rem (48px)

### Border Radius
- **Radius Sm**: 0.25rem (4px) - for small elements
- **Radius Md**: 0.375rem (6px) - for standard components
- **Radius Lg**: 0.5rem (8px) - for larger containers
- **Radius Xl**: 0.75rem (12px) - for prominent UI elements
- **Radius Full**: 9999px - for circular elements

### Shadow Definitions
- **Shadow Sm**: 0 1px 2px 0 rgba(0, 0, 0, 0.05) - subtle elevation
- **Shadow Md**: 0 4px 6px -3px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.05) - standard elevation
- **Shadow Lg**: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.05) - prominent elevation
- **Shadow Xl**: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05) - maximum elevation

### Animation Properties
- **Duration Fast**: 100ms - for quick micro-interactions
- **Duration Normal**: 200ms - for standard transitions
- **Duration Slow**: 300ms - for more pronounced animations
- **Ease In Out**: cubic-bezier(0.4, 0, 0.2, 1) - for smooth transitions
- **Ease Out**: cubic-bezier(0, 0, 0.2, 1) - for entrance animations

## API Contract Requirements (Frontend Perspective)

### Authentication Endpoints
- **POST /api/auth/login**: Handles user authentication, returns JWT
- **POST /api/auth/signup**: Handles user registration, returns JWT
- **POST /api/auth/logout**: Handles user logout, invalidates JWT

### Task Management Endpoints
- **GET /api/tasks**: Retrieve user's tasks with filtering options
- **POST /api/tasks**: Create a new task for the authenticated user
- **PUT /api/tasks/:id**: Update an existing task
- **DELETE /api/tasks/:id**: Delete a task
- **PATCH /api/tasks/:id/toggle-complete**: Toggle task completion status

## User Interaction States

### Loading States
- **Global Loading**: Full page overlay during major navigations
- **Component Loading**: Individual component spinners or skeleton screens
- **Optimistic Updates**: UI updates before API confirmation for smoother UX

### Error States
- **Field-Level Errors**: Inline validation messages
- **Form-Level Errors**: Top-level form error display
- **Network Errors**: Connectivity and server error handling
- **Permission Errors**: Unauthorized access handling

### Success States
- **Action Confirmations**: Toast notifications for successful actions
- **Progress Indicators**: Visual feedback for ongoing operations
- **Completion Feedback**: Visual confirmation for completed tasks

## Responsive Behaviors

### Mobile-First Breakpoints
- **Base (Mobile)**: Up to 768px - Single column, touch-optimized interactions
- **Tablet**: 768px - 1024px - May introduce dual-column layouts
- **Desktop**: 1024px+ - Full multi-column layouts with enhanced functionality

### Component Adaptations
- **Navigation**: From bottom bar (mobile) to sidebar (desktop)
- **Task Display**: From list (mobile) to card grid (desktop)
- **Form Layout**: From stacked (mobile) to horizontal arrangements (desktop)
- **Button Positioning**: From floating action (mobile) to header placement (desktop)
#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Colors for output
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
NC=$'\033[0m'

# Required template files for authentication
AUTH_TEMPLATES=(
    "src/views/Auth.vue"
    "src/views/Main.vue"
    "src/services/auth/auth.api.ts"
    "src/store/auth.store.ts"
    "src/router/index.ts"
)

# Additional GraphQL specific files
GRAPHQL_TEMPLATES=(
    "src/graphql/query.ts"
    "src/graphql/mutation.ts"
)

# Django specific files
DJANGO_TEMPLATES=(
    "vue.config.js"
    ".eslintrc.js"
    "package.json"
    "tsconfig.json"
    ".gitignore"
    "README.md"
)

# GraphQL specific files
GRAPHQL_CONFIG_FILES=(
    "vite.config.ts"
    "ionic.config.json"
    "capacitor.config.ts"
    ".browserslistrc"
    ".eslintrc.cjs"
    ".eslintignore"
    "cypress.config.ts"
    "tsconfig.node.json"
    "index.html"
)

# Trap for cleanup on script exit
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo -e "${RED}Script failed with exit code $exit_code${NC}"
        echo -e "${YELLOW}Cleaning up...${NC}"
        # Add cleanup commands here if needed
    fi
    exit $exit_code
}
trap cleanup EXIT

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "$1 is required but not installed. Please install it first."
    fi
}

# Function to check if directory exists
check_directory() {
    if [ ! -d "$1" ]; then
        error_exit "Directory $1 does not exist"
    fi
}

# Function to check if file exists
check_file() {
    if [ ! -f "$1" ]; then
        error_exit "File $1 does not exist"
    fi
}

# Function to validate port number
validate_port() {
    if ! [[ "$1" =~ ^[0-9]+$ ]] || [ "$1" -lt 1 ] || [ "$1" -gt 65535 ]; then
        error_exit "Port must be a number between 1 and 65535"
    fi
}

# Function to validate database name
validate_db_name() {
    if ! [[ "$1" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error_exit "Database name can only contain letters, numbers, and underscores"
    fi
}

# Function to validate database user
validate_db_user() {
    if ! [[ "$1" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error_exit "Database username can only contain letters, numbers, and underscores"
    fi
}

# Function to show error and exit
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Function to validate input
validate_input() {
    if [ -z "$1" ]; then
        error_exit "Input cannot be empty"
    fi
}

# Function to check dependencies
check_dependencies() {
    echo "Checking dependencies..."
    check_command "npm"
    check_command "python"
    check_command "psql"
    check_command "pip"
    echo -e "${GREEN}All dependencies are installed${NC}"
}

# Function to select frontend template type
select_frontend_template() {
    echo "Select frontend template type:"
    echo "1) Django REST API"
    echo "2) GraphQL"
    read -p "Enter choice (1-2): " frontend_choice

    case $frontend_choice in
        1) frontend_type="frontend-django" ;;
        2) frontend_type="frontend-graphql" ;;
        *) error_exit "Invalid frontend template choice" ;;
    esac

    echo -e "${GREEN}Selected $frontend_type template${NC}"
}

# Function to verify authentication templates
verify_auth_templates() {
    echo -e "${YELLOW}Verifying authentication templates...${NC}"
    
    # Check if template directory exists
    if [ ! -d "$SCRIPT_DIR/templates/$frontend_type" ]; then
        error_exit "Frontend template directory not found: $frontend_type"
    fi
    
    # Check frontend templates
    for template in "${AUTH_TEMPLATES[@]}"; do
        if [ ! -f "$SCRIPT_DIR/templates/$frontend_type/$template" ]; then
            error_exit "Missing required frontend template: $SCRIPT_DIR/templates/$frontend_type/$template"
        fi
    done
    
    # Check GraphQL specific templates if using GraphQL
    if [ "$frontend_type" = "frontend-graphql" ]; then
        for template in "${GRAPHQL_TEMPLATES[@]}"; do
            if [ ! -f "$SCRIPT_DIR/templates/$frontend_type/$template" ]; then
                error_exit "Missing required GraphQL template: $template"
            fi
        done
    fi
    
    # Check server templates
    if [ ! -d "$SCRIPT_DIR/templates/$server_type/server" ]; then
        error_exit "Server template directory not found: $SCRIPT_DIR/templates/$server_type/server"
    fi
    
    echo -e "${GREEN}All authentication templates verified${NC}"
}

# Function to setup environment variables for auth
setup_auth_env() {
    echo -e "${YELLOW}Setting up authentication environment variables...${NC}"
    
    # Add JWT settings to .env
    cat >> .env << EOL

# JWT Settings
JWT_SECRET_KEY=${secKey:-project_name}
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1

# API Settings
API_TYPE=${frontend_type}
EOL
    
    echo -e "${GREEN}Authentication environment variables configured${NC}"
}

frontend() {
    echo -e "${YELLOW}Setting up frontend...${NC}"
    
    # Select frontend template type
    select_frontend_template
    
    # Verify template directory exists before proceeding
    if [ ! -d "$SCRIPT_DIR/templates/$frontend_type" ]; then
        error_exit "Frontend template directory not found: $frontend_type"
    fi
    
    echo "Select Ionic template type:"
    echo "1) blank"
    echo "2) tabs"
    echo "3) sidemenu"
    read -p "Enter choice (1-3): " template_choice

    case $template_choice in
        1) template_type="blank" ;;
        2) template_type="tabs" ;;
        3) template_type="sidemenu" ;;
        *) error_exit "Invalid template choice" ;;
    esac

    # Create Ionic Vue project
    echo "Creating Ionic Vue project..."
    npm install -g @ionic/cli || error_exit "Failed to install Ionic CLI"
    ionic start frontend $template_type --type vue --no-git || confirm "Ionic exited setup"

    # Setup Vue/Ionic project structure
    cd frontend || error_exit "Failed to enter frontend directory"

    # Create necessary directories
    echo "Creating project directories..."
    for dir in views composables store services theme router; do
        mkdir -p "./src/$dir" || error_exit "Failed to create directory: src/$dir"
    done
    mkdir -p "./src/services/auth" || error_exit "Failed to create auth directory"
    
    # Create GraphQL specific directories if using GraphQL
    if [ "$frontend_type" = "frontend-graphql" ]; then
        mkdir -p "./src/graphql" || error_exit "Failed to create graphql directory"
    fi

    # Check if template directories exist
    echo "Verifying template directories..."
    for dir in store services/auth views theme router; do
        check_directory "$SCRIPT_DIR/templates/$frontend_type/src/$dir"
    done
    
    if [ "$frontend_type" = "frontend-graphql" ]; then
        check_directory "$SCRIPT_DIR/templates/$frontend_type/src/graphql"
    fi

    # Copy template files for auth flow
    echo "Copying frontend template files..."
    for dir in store services/auth views; do
        echo "Copying $dir files..."
        find "$SCRIPT_DIR/templates/$frontend_type/src/$dir" -type f -exec cp {} "./src/$dir/" \; || echo "Failed to copy $dir files"
    done
    
    # Copy GraphQL specific files if using GraphQL
    if [ "$frontend_type" = "frontend-graphql" ]; then
        echo "Copying GraphQL specific files..."
        find "$SCRIPT_DIR/templates/$frontend_type/src/graphql" -type f -exec cp {} ./src/graphql/ \; || echo "Failed to copy graphql files"
    fi
    
    # Copy individual files
    echo "Copying core files..."
    for file in App.vue main.ts; do
        if [ -f "$SCRIPT_DIR/templates/$frontend_type/src/$file" ]; then
            cp "$SCRIPT_DIR/templates/$frontend_type/src/$file" ./src/ || echo "Failed to copy $file"
        else
            echo "Warning: $file not found in template"
        fi
    done
    
    # Copy GraphQL specific source files
    if [ "$frontend_type" = "frontend-graphql" ]; then
        echo "Copying GraphQL specific source files..."
        for file in global.scss vue-shims.d.ts vite-env.d.ts; do
            if [ -f "$SCRIPT_DIR/templates/$frontend_type/src/$file" ]; then
                cp "$SCRIPT_DIR/templates/$frontend_type/src/$file" ./src/ || echo "Failed to copy $file"
            else
                echo "Warning: $file not found in template"
            fi
        done
    fi
    
    # Copy theme and router files
    echo "Copying theme and router files..."
    if [ -f "$SCRIPT_DIR/templates/$frontend_type/src/theme/variables.css" ]; then
        cp "$SCRIPT_DIR/templates/$frontend_type/src/theme/variables.css" ./src/theme/ || echo "Failed to copy theme"
    else
        echo "Warning: variables.css not found in template"
    fi
    
    if [ -f "$SCRIPT_DIR/templates/$frontend_type/src/router/index.ts" ]; then
        cp "$SCRIPT_DIR/templates/$frontend_type/src/router/index.ts" ./src/router/ || echo "Failed to copy router"
    else
        echo "Warning: router/index.ts not found in template"
    fi

    # Copy configuration files based on frontend type
    echo "Copying configuration files..."
    if [ "$frontend_type" = "frontend-django" ]; then
        for file in "${DJANGO_TEMPLATES[@]}"; do
            if [ -f "$SCRIPT_DIR/templates/$frontend_type/$file" ]; then
                cp "$SCRIPT_DIR/templates/$frontend_type/$file" ./ || echo "Failed to copy $file"
            else
                echo "Warning: $file not found in template"
            fi
        done
    else
        for file in "${GRAPHQL_CONFIG_FILES[@]}"; do
            if [ -f "$SCRIPT_DIR/templates/$frontend_type/$file" ]; then
                cp "$SCRIPT_DIR/templates/$frontend_type/$file" ./ || echo "Failed to copy $file"
            else
                echo "Warning: $file not found in template"
            fi
        done
    fi

    # Copy environment file
    if [ "$frontend_type" = "frontend-graphql" ] && [ -f "$SCRIPT_DIR/templates/$frontend_type/local.env" ]; then
        cp "$SCRIPT_DIR/templates/$frontend_type/local.env" ./.env || echo "Failed to copy environment file"
    fi

    # Install additional frontend dependencies
    echo "Installing additional frontend dependencies..."
    npm install || confirm "Failed to install dependencies"
    cd ../ || error_exit "Failed to return to parent directory"

    # Verify authentication templates
    verify_auth_templates
    
    echo -e "${GREEN}Frontend setup completed successfully${NC}"
}

server(){
    echo -e "${YELLOW}Setting up server...${NC}"
    # Create server directory
    mkdir -p server || error_exit "Failed to create server directory"
    mkdir -p server/"$project_name" || error_exit "Failed to create server directory"

    echo "Select server type:"
    echo "1) django"
    echo "2) fast-api"
    read -p "Enter choice (1-2): " server_choice

    case $server_choice in
        1) server_type="django-server" ;;
        2) server_type="fastapi-server" ;;
        *) error_exit "Invalid template choice" ;;
    esac

    # Check if template directories exist
    check_directory "$SCRIPT_DIR/templates/$server_type/server"

    # Copy server template files
    echo "Copying server template files..."
    cp -r "$SCRIPT_DIR/templates/$server_type/server/"* ./server/ || error_exit "Failed to copy server templates"
    cp "$SCRIPT_DIR/templates/$server_type/Pipfile" ./ || error_exit "Failed to copy Pipfile"
    cp "$SCRIPT_DIR/templates/$server_type/requirements.txt" ./ || error_exit "Failed to copy requirements"
    cp "$SCRIPT_DIR/templates/$server_type/.python-version" ./ || error_exit "Failed to copy python-version"

    # Setup pipenv
    echo "Setting up Python virtual environment..."
    cd server || error_exit "Failed to enter server directory"
    python -m pip install --user pipenv || error_exit "Failed to install pipenv"
    pipenv install || confirm "Failed to install Python dependencies"
    cd ../ || error_exit "Failed to return to parent directory"
    
    echo -e "${GREEN}Server setup completed successfully${NC}"
}

create_database(){
    echo -e "${YELLOW}Setting up database...${NC}"
    # Get database configuration
    echo "Database setup"
    echo "--------------"
    read -p "Enter database name: " db_name
    validate_input "$db_name"
    validate_db_name "$db_name"
    
    read -p "Enter database username: " db_user
    validate_input "$db_user"
    validate_db_user "$db_user"
    
    read -s -p "Enter database password: " db_password
    echo  # Add newline after password input
    validate_input "$db_password"

    # Create PostgreSQL database
    echo "Setting up PostgreSQL database..."
    psql -U "$db_user" -c "CREATE DATABASE $db_name;" || confirm "Failed to create database"

    # Setup environment variables
    echo "Setting up environment variables..."
    read -p "Enter server port (Default: 8000): " server_port
    server_port=${server_port:-"8000"}
    validate_port "$server_port"
    
    read -p "Enter a secret key: " secKey
    validate_input "$secKey"
    
    cat > .env << EOL
DB_NAME=${db_name:-""}
DB_USER=${db_user:-""}
DB_PASSWORD=${db_password:-""}
PORT=${server_port}
SESSION_SECRET=${secKey:-project_name}
EOL

    # Setup authentication environment variables
    setup_auth_env
    
    echo -e "${GREEN}Database setup completed successfully${NC}"
}

# Add instructions for authentication testing
print_auth_instructions() {
    echo -e "${GREEN}Authentication Setup Complete!${NC}"
    echo "To test the authentication:"
    echo "1. Start the server: cd $project_name/server && pipenv run python manage.py runserver"
    echo "2. Start the frontend: cd $project_name/frontend && npm run serve"
    echo "3. Open http://localhost:8100 in your browser"
    echo "4. You should see the login page"
    echo "5. Create a new account using the register page"
    echo "6. After registration, you'll be redirected to the home page"
    echo "7. You can now log in and out using the authentication system"
}

# Welcome message
echo -e "${GREEN}Welcome to Full-Stack App Generator${NC}"
echo "--------------------------------"

# Check dependencies before starting
check_dependencies

# Get project name
read -p "Enter project name (lowercase, no spaces): " project_name
validate_input "$project_name"

# Validate project name format
if [[ ! $project_name =~ ^[a-z0-9-]+$ ]]; then
    error_exit "Project name must be lowercase with no spaces (only hyphens allowed)"
fi

# Create project structure
echo "Creating project structure..."
mkdir -p "$project_name" || error_exit "Failed to create project directory"
cd "$project_name" || error_exit "Failed to enter project directory"

if [ "$1" == "server" ]; then
    server
    create_database
    find . -type f -exec sed -i "s/appname/$project_name/g" {} +
elif [ "$1" == "database" ]; then
    create_database
else
    frontend
    server
    create_database
    find . -type f -exec sed -i "s/appname/$project_name/g" {} +
fi

print_auth_instructions
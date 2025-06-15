# Nexus Manager

---

## 📝 Overview

**Nexus Manager** is a cross-platform tool for managing Nexus Repository and IQ Server, providing a REST API interface. It is distributed as a standalone executable for Windows, macOS, and Linux—no Python installation required.

---

## 📦 Using the Release Executable

### 1. Download & Extract

- Download the appropriate archive for your platform from the release page.
- Extract the archive. You will get a folder containing:
  - The executable (`nexus-manager` or `nexus-manager.exe`)
  - `config/` (configuration files)
  - `pyproject.toml`
  - `README.md`

### 2. Configure Environment

- Copy `config/.env.example` to `config/.env` and fill in your server details and secrets.

### 3. Run the Application

- **REST API:**
  - On Linux/macOS: `./nexus-manager`
  - On Windows: `nexus-manager.exe`
  - API endpoints available at `http://localhost:5000/api/`

---

## 🔌 REST API

### Base URL

```
http://localhost:5000/api
```

### Authentication

The REST API uses configuration from the `.env` file. Ensure your `.env` file is properly configured with Nexus and IQ Server credentials.

### Endpoints

#### 1. Health Check

```http
GET /api/health
```

**Response:**

```json
{
  "success": true,
  "status": "healthy",
  "version": "1.0.0"
}
```

---

#### 2. Get Configuration

```http
GET /api/config
```

**Response:**

```json
{
  "success": true,
  "data": {
    "organizations": [
      {
        "id": "org1",
        "name": "Organization 1",
        "chineseName": "組織一"
      }
    ],
    "package_managers": [
      "apt",
      "docker",
      "maven2",
      "npm",
      "nuget",
      "pypi",
      "yum"
    ],
    "shared_package_managers": ["npm", "maven2", "nuget", "yum", "raw"]
  }
}
```

---

#### 3. Create Repository

```http
POST /api/repository
Content-Type: application/json
```

**Request Body:**

```json
{
  "organization_name_chinese": "後勤應用系統部",
  "ldap_username": "john.doe",
  "package_manager": "npm",
  "shared": false,
  "app_id": "my-app"
}
```

**Request Fields:**

- `organization_name_chinese` (`string`, required): Organization's Chinese name for IQ Server role assignment
- `ldap_username` (`string`, required): LDAP username for repository access
- `package_manager` (`string`, required): Package manager type (npm, maven2, etc.)
- `shared` (`boolean`, optional): Whether to use shared repository (default: false)
- `app_id` (`string`, required if shared=false): Application ID for repository naming

**Response:**

```json
{
  "success": true,
  "data": {
    "action": "create",
    "repository_name": "npm-release-my-app",
    "ldap_username": "john.doe",
    "organization_id": "0a4006e9236c4ede89cfec9a25211e02",
    "package_manager": "npm",
    "shared": false,
    "app_id": "my-app"
  },
  "message": "Successfully created repository and privileges."
}
```

---

#### 4. Delete Repository

```http
DELETE /api/repository
Content-Type: application/json
```

**Request Body:** Same as Create Repository

**Response:**

```json
{
  "success": true,
  "data": {
    "action": "delete",
    "repository_name": "npm-release-my-app",
    "ldap_username": "john.doe",
    "organization_id": "org1",
    "package_manager": "npm",
    "shared": false,
    "app_id": "my-app"
  },
  "message": "Successfully deleted repository and privileges."
}
```

---

#### 5. API Documentation

```http
GET /api/docs
```

Returns the complete API documentation in JSON format.

---

### Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error description"
}
```

**Common HTTP status codes:**

- `400`: Bad Request (missing required fields, invalid data)
- `500`: Internal Server Error (configuration issues, API failures)

---

### Example Usage

#### Using `curl`:

- **Create a shared repository:**

  ```bash
  curl -X POST http://localhost:5000/api/repository \
    -H "Content-Type: application/json" \
    -d '{
      "organization_name_chinese": "後勤應用系統部",
      "ldap_username": "john.doe",
      "package_manager": "npm",
      "shared": true
    }'
  ```

- **Create an app-specific repository:**

  ```bash
  curl -X POST http://localhost:5000/api/repository \
    -H "Content-Type: application/json" \
    -d '{
      "organization_id": "org1",
      "ldap_username": "john.doe",
      "package_manager": "maven2",
      "shared": false,
      "app_id": "my-java-app"
    }'
  ```

- **Delete a repository:**

  ```bash
  curl -X DELETE http://localhost:5000/api/repository \
    -H "Content-Type: application/json" \
    -d '{
      "organization_id": "org1",
      "ldap_username": "john.doe",
      "package_manager": "npm",
      "shared": false,
      "app_id": "my-app"
    }'
  ```

#### Using Python `requests`:

```python
import requests

# Configuration
api_base = "http://localhost:5000/api"

# Create repository
response = requests.post(f"{api_base}/repository", json={
    "organization_name_chinese": "後勤應用系統部",
    "ldap_username": "john.doe",
    "package_manager": "npm",
    "shared": False,
    "app_id": "my-app"
})

if response.status_code == 200:
    result = response.json()
    print(f"Success: {result['message']}")
else:
    error = response.json()
    print(f"Error: {error['error']}")
```

---

## 🎨 Customization

### Configuration

- All configuration is in the `config/` directory.
- Edit `config/.env` for environment variables (see `.env.example` for options).
- Edit `config/organisations.json` and `config/package_manager_config.json` for organization and package manager settings.

---

## 🛠️ Codebase Maintenance

### Structure

- `nexus_manager.py`: Main entry point and REST API endpoints.
- `nexus_manager/`: Core logic and utilities.
  - `core.py`: Main business logic.
  - `utils.py`: Helper functions.
  - `error_handler.py`: Error handling.
- `config/`: Configuration files.

### Adding Features

- Add new logic in `nexus_manager/` as needed.
- Register new API endpoints in `nexus_manager.py`.
- Update API documentation in the `/api/docs` endpoint.

### Dependency Management

- Dependencies are managed with [uv](https://github.com/astral-sh/uv) and listed in `pyproject.toml`.
- To add a dependency:
  1. Install [uv](https://github.com/astral-sh/uv) locally.
  2. Run `uv pip install <package>`.
  3. Update `pyproject.toml` and commit changes.

### Building the Executable

- Builds are automated via GitHub Actions.
- To build locally:
  1. Install [uv](https://github.com/astral-sh/uv) and [pyinstaller](https://pyinstaller.org/).
  2. Run the build command as in `.github/workflows/build-release.yml`.

---

## 💬 Support

- For issues, open a GitHub issue in this repository.
- For configuration help, see comments in `config/.env.example`.

---

## 📄 License

See `LICENSE` file (if present) for license information.

---

## ⚙️ Repository Creation & Deletion Logic

This section explains the steps and logic followed by Nexus Manager when creating or deleting a repository via the REST API or CLI.

### Creation Flow

1. **Input Validation**
   - Required fields: `organization_name_chinese`, `ldap_username`, `package_manager` (and `app_id` if not shared).
   - Organization is looked up by its Chinese name.
   - The package manager is validated against supported formats.
2. **Configuration Loading**
   - Loads environment variables and configuration files from the `config/` directory.
   - Determines repository, privilege, and role names based on input and conventions.
3. **Repository Creation**
   - Checks if the repository already exists in Nexus.
   - If not, creates a new proxy repository with the specified package manager and remote URL.
4. **Privilege Creation**
   - Checks if the required privilege exists.
   - If not, creates a new privilege for the repository.
5. **Role and User Setup**
   - Ensures a role exists for the user and assigns the privilege to it.
   - Ensures the user exists and is assigned the correct role(s).
6. **IQ Server Role Assignment** (if organization is specified)
   - Looks up the corresponding IQ Server role.
   - Grants the role to the user for the organization.
7. **Success Response**
   - Returns a JSON response with details of the created resources.

### Deletion Flow

1. **Input Validation & Configuration Loading**
   - Same as in creation.
2. **Role and IQ Server Cleanup**
   - Removes the privilege from the role and unassigns the role from the user.
   - Revokes the IQ Server role from the user (if applicable).
3. **Privilege and Repository Deletion**
   - Deletes the privilege and then the repository from Nexus.
4. **Success Response**
   - Returns a JSON response confirming deletion.

### Error Handling

- All steps use robust error handling and return consistent error responses with details and appropriate HTTP status codes.
- Common errors include missing fields, invalid configuration, or API failures.

---

## 🏷️ Naming Convention

Nexus Manager uses a consistent naming convention for repositories, privileges, and roles to ensure clarity and avoid conflicts.

### Repository Name

- **Shared repository:**
  - Format: `<package_manager>-release-shared`
  - Example: `npm-release-shared`
- **App-specific repository:**
  - Format: `<package_manager>-release-<app_id>`
  - Example: `maven2-release-my-java-app`

### Privilege Name

- The privilege name is always the same as the repository name.
  - Example: `npm-release-shared`, `maven2-release-my-java-app`

### Role Name

- The role name is set to the LDAP username of the user who will access the repository.
  - Example: `john.doe`

### Summary Table

| Type       | Format                               | Example                      |
| ---------- | ------------------------------------ | ---------------------------- |
| Repository | `<package_manager>-release-shared`   | `npm-release-shared`         |
| Repository | `<package_manager>-release-<app_id>` | `maven2-release-my-java-app` |
| Privilege  | same as repository name              | `npm-release-shared`         |
| Role       | `<ldap_username>`                    | `john.doe`                   |

---

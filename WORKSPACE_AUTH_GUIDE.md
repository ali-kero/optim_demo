# Databricks Workspace Authentication Guide

This guide shows you how to connect to Databricks workspaces using OAuth (browser-based authentication).

## Your Current Workspaces

You have the following workspaces configured in `~/.databrickscfg`:

- **DEFAULT**: `https://adb-984752964297111.11.azuredatabricks.net/`
- **field-eng-azure**: `https://adb-984752964297111.11.azuredatabricks.net/`
- **ubisoft**: `https://adb-1306912788495007.7.azuredatabricks.net/`
- **ONEENVPERSO**: `https://dbc-0e4dc532-0396.cloud.databricks.com/`
- **e2-demo-field-eng**: `https://e2-demo-field-eng.cloud.databricks.com`
- **e2-dogfood**: `https://e2-dogfood.staging.cloud.databricks.com`
- **DOGFOOD**: `https://e2-dogfood.staging.cloud.databricks.com/`

## 🌐 Add a New Workspace with OAuth (Browser)

### Step 1: Authenticate with Browser

```bash
# Activate your virtual environment first
source .venv/bin/activate

# Login to a new workspace with OAuth
databricks auth login --host https://your-workspace.cloud.databricks.com --profile <profile-name>

# Example:
databricks auth login --host https://adb-123456789.azuredatabricks.net --profile my-new-workspace
```

This will:
1. Open your browser automatically
2. Ask you to log in to Databricks
3. Save the authentication to `~/.databrickscfg`

### Step 2: Verify Authentication

```bash
# Test the connection
databricks workspace list --profile my-new-workspace

# Or set as default for the current session
export DATABRICKS_CONFIG_PROFILE=my-new-workspace
databricks workspace list
```

## 📝 Usage with `databricks.yml`

Your `databricks.yml` is now configured to work with multiple workspaces. Here's how to use different workspaces:

### Option 1: Using Targets (Recommended)

```bash
# Use the default dev workspace (DEFAULT profile)
databricks bundle deploy

# Use field-eng-azure workspace
databricks bundle deploy -t field-eng-azure

# Use ubisoft workspace
databricks bundle deploy -t ubisoft
```

### Option 2: Using Environment Variable

```bash
# Set which profile to use
export DATABRICKS_CONFIG_PROFILE=field-eng-azure

# Now all commands use that profile
databricks workspace list
databricks bundle deploy
```

### Option 3: Using --profile Flag

```bash
# Use profile directly in commands
databricks workspace list --profile field-eng-azure
databricks clusters list --profile ubisoft
```

## 🔄 Switch Between Workspaces

### Quick Switch Script

Create this helper script `switch-workspace.sh`:

```bash
#!/bin/bash
# switch-workspace.sh - Helper to switch Databricks workspaces

case "$1" in
  "default")
    export DATABRICKS_CONFIG_PROFILE=DEFAULT
    echo "✅ Switched to DEFAULT workspace"
    ;;
  "field-eng")
    export DATABRICKS_CONFIG_PROFILE=field-eng-azure
    echo "✅ Switched to field-eng-azure workspace"
    ;;
  "ubisoft")
    export DATABRICKS_CONFIG_PROFILE=ubisoft
    echo "✅ Switched to ubisoft workspace"
    ;;
  *)
    echo "Available workspaces:"
    echo "  default      - DEFAULT profile"
    echo "  field-eng    - field-eng-azure profile"
    echo "  ubisoft      - ubisoft profile"
    echo ""
    echo "Usage: source switch-workspace.sh <workspace>"
    ;;
esac

# Show current profile
if [ ! -z "$DATABRICKS_CONFIG_PROFILE" ]; then
  echo "Current profile: $DATABRICKS_CONFIG_PROFILE"
fi
```

Make it executable and use it:

```bash
chmod +x switch-workspace.sh

# Use it (note: use 'source' to set env vars in current shell)
source switch-workspace.sh field-eng
source switch-workspace.sh ubisoft
source switch-workspace.sh default
```

## 🆕 Add New Workspace to databricks.yml

To add a new workspace target, edit `databricks.yml`:

```yaml
targets:
  my-new-workspace:
    mode: development
    workspace:
      profile: my-new-workspace  # Must match profile name in ~/.databrickscfg
      root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
```

Then use it:

```bash
databricks bundle deploy -t my-new-workspace
```

## 🔐 OAuth vs Token Authentication

| Method | Pros | Cons |
|--------|------|------|
| **OAuth (Browser)** | ✅ More secure<br>✅ Auto-refresh<br>✅ No token management<br>✅ Uses your user account | ❌ Requires browser access |
| **Token** | ✅ Works without browser<br>✅ Good for CI/CD | ❌ Must manually rotate<br>❌ Less secure<br>❌ Can expire |

**Recommendation**: Use OAuth for development, tokens for CI/CD pipelines.

## 🔧 Troubleshooting

### Issue: "Authentication configuration not found"

```bash
# List all profiles
databricks auth profiles

# Re-authenticate
databricks auth login --host <your-host> --profile <profile-name>
```

### Issue: "Token expired"

OAuth tokens auto-refresh! But if you have issues:

```bash
# Re-login
databricks auth login --profile <profile-name>
```

### Issue: "Which workspace am I using?"

```bash
# Check current configuration
databricks auth describe

# Or check environment
echo $DATABRICKS_CONFIG_PROFILE

# List all profiles
cat ~/.databrickscfg
```

### Issue: "Can't connect to workspace"

```bash
# Verify the workspace URL is correct
databricks workspace list --profile <profile-name> --debug
```

## 💡 Best Practices

1. **Use descriptive profile names**: `prod-workspace`, `dev-workspace`, `client-workspace`
2. **Set DEFAULT profile**: Your most-used workspace
3. **Use targets in databricks.yml**: Easier to manage multiple workspaces
4. **Document workspaces**: Keep a list of what each profile is for
5. **Use OAuth when possible**: More secure and convenient

## 📚 Common Commands

```bash
# List all configured profiles
databricks auth profiles

# Show current authentication details
databricks auth describe

# Login to new workspace
databricks auth login --host <url> --profile <name>

# Use specific profile for a command
databricks <command> --profile <profile-name>

# Set default profile for session
export DATABRICKS_CONFIG_PROFILE=<profile-name>

# Deploy to specific workspace
databricks bundle deploy -t <target-name>

# List clusters in specific workspace
databricks clusters list --profile <profile-name>

# List jobs in specific workspace
databricks jobs list --profile <profile-name>
```

## 🚀 Quick Reference

### Add New Workspace (Interactive)

```bash
source .venv/bin/activate
databricks auth login
```

This will prompt you for:
1. Workspace URL
2. Profile name (optional)

Then open your browser to complete authentication!

### Add New Workspace (One Command)

```bash
databricks auth login --host https://your-workspace.cloud.databricks.com --profile my-workspace
```

### Test Connection

```bash
databricks workspace list --profile my-workspace
```

### Use in Your Code

When using VS Code with Databricks extension, select the profile from the status bar!

---

**Need help?** Check the [Databricks CLI Authentication docs](https://docs.databricks.com/dev-tools/cli/authentication.html)


#!/usr/bin/env bash

# Usage: ./bump_version.sh [major|minor|patch]
# Example: ./bump_version.sh patch

set -e

if [ -z "$1" ]; then
  echo "Usage: ./bump_version.sh [major|minor|patch]"
  exit 1
fi

PART=$1

# 1. Ensure the tree is clean
if [[ -n $(git status -s) ]]; then
  echo "Error: Git working directory not clean. Commit changes first."
  exit 1
fi

# 2. Bump version in a VERSION file (simple approach) or pyproject.toml
# If you don't have a VERSION file yet, create one with "0.1.0"
if [ ! -f VERSION ]; then
  echo "0.1.0" > VERSION
fi

CURRENT_VERSION=$(cat VERSION)
IFS='.' read -r -a PARTS <<< "$CURRENT_VERSION"
MAJOR=${PARTS[0]}
MINOR=${PARTS[1]}
PATCH=${PARTS[2]}

case $PART in
  major) MAJOR=$((MAJOR+1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR+1)); PATCH=0 ;;
  patch) PATCH=$((PATCH+1)) ;;
  *) echo "Invalid argument. Use major, minor, or patch."; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "$NEW_VERSION" > VERSION

# Update pyproject.toml version
if [ -f pyproject.toml ]; then
  # Use sed to update the version line in pyproject.toml
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS sed requires -i with empty string
    sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
  else
    # Linux sed
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
  fi
  echo "Updated pyproject.toml to version $NEW_VERSION"
fi

# Optional: Update __init__.py if you have one
# sed -i "s/__version__ = .*/__version__ = \"$NEW_VERSION\"/" src/__init__.py

# 3. Commit and Tag
echo "Bumping version from $CURRENT_VERSION to $NEW_VERSION"
git add VERSION pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

# 4. Push
echo "Pushing to origin..."
git push origin main "v$NEW_VERSION"

echo "Done! Nix flake users can now update to v$NEW_VERSION"

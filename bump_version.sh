#!/usr/bin/env bash

# Usage: ./bump_version.sh [major|minor|patch]
# Example: ./bump_version.sh minor
# 
# This script will:
# 1. Check git working directory is clean
# 2. Run tests to ensure everything passes
# 3. Bump the version in VERSION and pyproject.toml
# 4. Commit the version bump
# 5. Create a git tag
# 6. Push to origin with tags

set -e

if [ -z "$1" ]; then
  echo "Usage: ./bump_version.sh [major|minor|patch]"
  exit 1
fi

PART=$1

echo "🔍 Step 1: Checking git status..."
# 1. Ensure the tree is clean
if [[ -n $(git status -s) ]]; then
  echo "❌ Error: Git working directory not clean. Commit changes first."
  git status -s
  exit 1
fi
echo "✅ Git working directory is clean"

echo ""
echo "🧪 Step 2: Running tests..."
# 2. Run tests
if ! pytest tests/ -v; then
  echo "❌ Error: Tests failed. Fix tests before bumping version."
  exit 1
fi
echo "✅ All tests passed"

echo ""
echo "📝 Step 3: Bumping version..."
# 3. Bump version
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
  *) echo "❌ Invalid argument. Use major, minor, or patch."; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "$NEW_VERSION" > VERSION
echo "✅ Version bumped from $CURRENT_VERSION to $NEW_VERSION"

# 4. Update pyproject.toml version
if [ -f pyproject.toml ]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
  else
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
  fi
  echo "✅ Updated pyproject.toml to version $NEW_VERSION"
fi

echo ""
echo "💾 Step 4: Committing changes..."
# 5. Commit and Tag
git add VERSION pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
echo "✅ Changes committed"

echo ""
echo "🏷️  Step 5: Creating git tag..."
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
echo "✅ Tag v$NEW_VERSION created"

echo ""
echo "🚀 Step 6: Pushing to origin..."
# 6. Push
git push origin main --tags
echo "✅ Pushed to origin with tags"

echo ""
echo "🎉 Done! Version $NEW_VERSION has been released."
echo "   - Committed version bump"
echo "   - Tagged as v$NEW_VERSION"
echo "   - Pushed to origin"

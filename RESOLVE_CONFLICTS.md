# Conflict Resolution Guide

## Quick Resolution Steps

### Step 1: Check Current Status

```bash
git status
```

### Step 2: Fetch Latest Changes

```bash
git fetch origin
```

### Step 3: Merge with Master

```bash
git merge origin/master
```

### Step 4: If Conflicts Found

Look for files with conflict markers:

- `<<<<<<< HEAD` - Your changes
- `=======` - Separator
- `>>>>>>> origin/master` - Their changes

### Step 5: Resolve Each Conflict

For each conflicted file:

1. Open the file
2. Find conflict markers
3. Choose which changes to keep (or merge both)
4. Remove conflict markers
5. Save the file

### Step 6: Mark as Resolved

```bash
git add <resolved-file>
```

### Step 7: Complete the Merge

```bash
git commit -m "Resolve merge conflicts"
```

### Step 8: Push

```bash
git push
```

---

## Common Conflict Files (Already Resolved)

Based on code review, these files should be conflict-free:

- ✅ `backend/main.py` - All routers registered
- ✅ `backend/models/models.py` - All models included
- ✅ `backend/routes/auth.py` - Email normalization fixed
- ✅ `backend/routes/goals.py` - Water tracking added
- ✅ `backend/routes/provider.py` - Provider routes added
- ✅ `backend/routes/credentials.py` - Credentials route added

---

## Manual Resolution Guide

If conflicts are found, resolve them by:

1. **Keep your changes**: Remove their section, keep yours
2. **Keep their changes**: Remove your section, keep theirs
3. **Merge both**: Combine both sets of changes logically

Example resolution:

```
<<<<<<< HEAD
your code here
=======
their code here
>>>>>>> origin/master
```

Should become:

```
your merged code here (combining both)
```

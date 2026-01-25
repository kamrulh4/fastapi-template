# Aerich Migrations Guide

Aerich is a database migrations management tool for Tortoise ORM.

## Setup Aerich

If Aerich is not already initialized for the project:

```bash
aerich init -t app.core.db.TORTOISE_ORM
```

## Initial Migration

To create the initial database structure:

```bash
aerich init-db
```

## Create New Migration

Run this whenever you make changes to your models:

```bash
aerich migrate --name <migration_name>
```

## Apply Migrations

To upgrade the database to the latest version:

```bash
aerich upgrade
```

## Revert Migrations

To downgrade the database:

```bash
aerich downgrade
```

## History

To view the migration history:

```bash
aerich history
```

## Inspection

To see the current migration state:

```bash
aerich inspect
```

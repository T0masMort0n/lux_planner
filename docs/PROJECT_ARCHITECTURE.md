PROJECT_ARCHITECTURE.md
Layered Structure

System Layer

AppShell

UI primitives

Theme system

Navigation

Feature Layer

Journal

Scheduler

Meals

Exercise

Goals

Core Layer

Settings

Storage

Shared utilities

Features never import each other.
All communication happens via system-level services.
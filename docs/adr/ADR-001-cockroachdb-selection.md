# ADR-001: Database Selection

## Status

Accepted

## Context

CareerOS requires a database system to store:

- User profiles
- Conversations
- AI memories
- Agent interactions

The system should support scalability, reliability, and future cloud deployment.

## Considered Options

## PostgreSQL

### Pros

- Mature relational database
- Large community
- Strong ecosystem
- Excellent reliability

### Cons

- Scaling requires additional configuration

---

## MongoDB

### Pros

- Flexible document-based storage
- Easy JSON representation

### Cons

- Complex relationships become harder to manage

---

## CockroachDB

### Pros

- PostgreSQL compatible
- Distributed SQL database
- High availability
- Cloud-native architecture
- Automatic replication

### Cons

- Requires understanding distributed database concepts

---

## Decision

We selected CockroachDB as the database solution for CareerOS.

The main reasons are:

- PostgreSQL compatibility
- Scalability
- Distributed architecture
- Suitability for cloud-based applications

## Consequences

### Positive

- Better scalability for future growth
- Reliable storage for AI memory
- Cloud-ready architecture

### Negative

- Additional learning complexity
- Distributed database concepts must be considered
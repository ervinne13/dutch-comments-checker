## Mermaid API Flow

```mermaid
graph TD
    A[API receives comment check request] --> B{Is comment safe?}
    B -- Yes --> C[Comment is shown]
    B -- No, flagged for moderation --> D[Return flagged status Comment is NOT shown yet]
    D --> E[Background moderation process 4-6s]
    E --> F[Moderation result available]
    F --> G[Show comment if approved, or take action if rejected]
# FastAPI app workflow

```mermaid
flowchart LR
  subgraph Client[Client]
    U[User / Browser]
  end
  subgraph Server[FastAPI app (webapp/main.py)]
    A[GET /  (root) -> FileResponse(index.html)]
    B[POST /generate -> Body(length)]
    C[Validate Body.length]
    D[os.urandom -> base64.b64encode -> slice & decode]
    E[Return JSON {"token": string}]
    F[Mount /ui -> StaticFiles(static/)]
  end

  U -->|GET /| A
  A -->|serves index.html| U
  U -->|AJAX POST /generate {length}| B
  B --> C
  C --> D
  D --> E
  E -->|response| U
  Server --> F
```

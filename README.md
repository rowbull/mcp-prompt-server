# Quin MCP Prompt Server

This server manages conversation prompts and localization for Quin's financial advisor AI. It decouples conversation logic from the core LLM, enabling global scalability.

## Running the Server

1.  Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2.  Run the Flask development server:
    ```
    python app.py
    ```

The server will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Health Check

-   **URL**: `/health`
-   **Method**: `GET`
-   **Success Response**:
    -   **Code**: 200
    -   **Content**: `{"status": "ok"}`

### Get Prompt Instructions

This is the main endpoint for the Quin Edge Function to call.

-   **URL**: `/mcp/getPromptInstructions`
-   **Method**: `POST`
-   **Data Params**:
    ```json
    {
      "country": "US",
      "language": "en",
      "sessionType": "session1",
      "userContext": {}
    }
    ```
-   **Success Response**:
    -   **Code**: 200
    -   **Content**: A JSON object with the full conversation instructions.

### Test Endpoint

A simple GET endpoint for quick testing.

-   **URL**: `/test/prompt?country=US&language=en&session=session1`
-   **Method**: `GET`
-   **Success Response**:
    -   **Code**: 200
    -   **Content**: A JSON object with the full conversation instructions.

---

## Integration Documentation

To integrate this MCP server with the Quin Supabase Edge Function, the function should be modified to make a `POST` request to the `/mcp/getPromptInstructions` endpoint instead of using a hardcoded prompt.

**Example Edge Function (JavaScript):**

```javascript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  // Assuming you have user data and session info
  const userProfile = { ... };
  const sessionType = 'session1';
  const userLanguage = 'en'; // or 'es'
  const userCountry = 'US';

  const mcpResponse = await fetch('YOUR_MCP_SERVER_URL/mcp/getPromptInstructions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      country: userCountry,
      language: userLanguage,
      sessionType: sessionType,
      userContext: userProfile,
    }),
  });

  const promptData = await mcpResponse.json();

  // Now use promptData to construct the prompt for the LLM
  // e.g., pass promptData.instructions to the LLM

  return new Response(
    JSON.stringify(promptData),
    { headers: { "Content-Type": "application/json" } },
  )
})
```

## Expansion Guide

Adding a new country or language is straightforward.

### Adding a new Language

1.  **Create Prompt File**: Add a new prompt file in `mcp_server/prompts/`. For example, for French in the US, create `us_fr_session1.txt`.
2.  **Update Available Languages**: In `mcp_server/logic.py`, update the `get_available_languages` function to include the new language for the respective country.

### Adding a new Country

1.  **Create Context File**: Add a new financial context file in `mcp_server/context/`. For example, for Canada, create `ca_context.json`.
2.  **Create Prompt Files**: Add prompt files for the new country in `mcp_server/prompts/`. For example, `ca_en_session1.txt`.
3.  **Update Available Languages**: In `mcp_server/logic.py`, add the new country and its supported languages to the `get_available_languages` function.
```

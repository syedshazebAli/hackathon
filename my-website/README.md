# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## AI Chatbot (Gemini) Setup

1. Create a `.env` file at the project root with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

2. Start the dev server with the env loaded:

- Windows (PowerShell): `$env:GEMINI_API_KEY='your_api_key_here'; yarn start`
- Windows (cmd): `set GEMINI_API_KEY=your_api_key_here && yarn start`

3. Build also requires the env var present in the shell:

- PowerShell: `$env:GEMINI_API_KEY='your_api_key_here'; yarn build`
- cmd: `set GEMINI_API_KEY=your_api_key_here && yarn build`

The chatbot uses Google Gemini free-tier via the REST API and follows a constrained system prompt to reduce hallucinations. If rate limits are reached, the UI shows a friendly message. The floating button appears on all pages, and the UI inherits theme variables for a Notion-like appearance with dark mode support.

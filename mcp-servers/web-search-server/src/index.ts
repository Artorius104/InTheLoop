#!/usr/bin/env node

/**
 * Web Search MCP Server
 * Provides web search capabilities via Serper API
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const SERPER_API = 'https://google.serper.dev';

class WebSearchServer {
  private server: Server;
  private apiKey: string | undefined;

  constructor() {
    this.apiKey = process.env.SERPER_API_KEY;
    
    this.server = new Server(
      {
        name: 'web-search-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'search_web',
          description: 'Search the web using Google',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              num: {
                type: 'number',
                description: 'Number of results (default: 10)',
                default: 10,
              },
              type: {
                type: 'string',
                enum: ['search', 'news', 'images', 'videos'],
                description: 'Type of search',
                default: 'search',
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'search_news',
          description: 'Search for news articles',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              num: {
                type: 'number',
                default: 10,
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      if (!this.apiKey) {
        return {
          content: [
            {
              type: 'text',
              text: 'Error: SERPER_API_KEY not configured',
            },
          ],
        };
      }

      try {
        if (name === 'search_web') {
          return await this.searchWeb(args);
        } else if (name === 'search_news') {
          return await this.searchNews(args);
        } else {
          throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [{ type: 'text', text: `Error: ${errorMessage}` }],
        };
      }
    });
  }

  private async searchWeb(args: any) {
    const { query, num = 10, type = 'search' } = args;

    const endpoint = type === 'search' ? '/search' : `/${type}`;
    const url = `${SERPER_API}${endpoint}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'X-API-KEY': this.apiKey!,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ q: query, num }),
    });

    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  private async searchNews(args: any) {
    const { query, num = 10 } = args;

    const response = await fetch(`${SERPER_API}/news`, {
      method: 'POST',
      headers: {
        'X-API-KEY': this.apiKey!,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ q: query, num }),
    });

    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Web Search MCP Server running on stdio');
  }
}

const server = new WebSearchServer();
server.run().catch(console.error);


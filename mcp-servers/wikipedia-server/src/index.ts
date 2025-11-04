#!/usr/bin/env node

/**
 * Wikipedia MCP Server
 * Provides access to Wikipedia articles
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const WIKIPEDIA_API = 'https://en.wikipedia.org/w/api.php';

class WikipediaServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'wikipedia-server',
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
          name: 'search_wikipedia',
          description: 'Search Wikipedia articles',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              limit: {
                type: 'number',
                description: 'Maximum number of results',
                default: 10,
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'get_article',
          description: 'Get a Wikipedia article content',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'Article title',
              },
            },
            required: ['title'],
          },
        },
        {
          name: 'get_summary',
          description: 'Get a summary of a Wikipedia article',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'Article title',
              },
            },
            required: ['title'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'search_wikipedia') {
          return await this.searchWikipedia(args.query as string, args.limit as number);
        } else if (name === 'get_article') {
          return await this.getArticle(args.title as string);
        } else if (name === 'get_summary') {
          return await this.getSummary(args.title as string);
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

  private async searchWikipedia(query: string, limit: number = 10) {
    const url = new URL(WIKIPEDIA_API);
    url.searchParams.append('action', 'opensearch');
    url.searchParams.append('search', query);
    url.searchParams.append('limit', limit.toString());
    url.searchParams.append('format', 'json');

    const response = await fetch(url.toString());
    const data = await response.json();

    const [searchTerm, titles, descriptions, urls] = data as [string, string[], string[], string[]];
    
    const results = titles.map((title, i) => ({
      title,
      description: descriptions[i],
      url: urls[i],
    }));

    return {
      content: [{ type: 'text', text: JSON.stringify(results, null, 2) }],
    };
  }

  private async getArticle(title: string) {
    const url = new URL(WIKIPEDIA_API);
    url.searchParams.append('action', 'query');
    url.searchParams.append('prop', 'extracts');
    url.searchParams.append('titles', title);
    url.searchParams.append('format', 'json');
    url.searchParams.append('explaintext', '1');

    const response = await fetch(url.toString());
    const data: any = await response.json();

    const pages = data.query.pages;
    const page = Object.values(pages)[0] as any;

    if (page.missing) {
      throw new Error(`Article "${title}" not found`);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            title: page.title,
            content: page.extract,
          }, null, 2),
        },
      ],
    };
  }

  private async getSummary(title: string) {
    const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(title)}`;

    const response = await fetch(url);
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Wikipedia MCP Server running on stdio');
  }
}

const server = new WikipediaServer();
server.run().catch(console.error);


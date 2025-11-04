#!/usr/bin/env node

/**
 * News MCP Server
 * Provides access to news and press articles
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const NEWS_API = 'https://newsapi.org/v2';

class NewsServer {
  private server: Server;
  private apiKey: string | undefined;

  constructor() {
    this.apiKey = process.env.NEWS_API_KEY;
    
    this.server = new Server(
      {
        name: 'news-server',
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
          name: 'search_news',
          description: 'Search for news articles',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              language: {
                type: 'string',
                description: 'Language (en, fr, etc.)',
                default: 'en',
              },
              sortBy: {
                type: 'string',
                enum: ['relevancy', 'popularity', 'publishedAt'],
                default: 'relevancy',
              },
              pageSize: {
                type: 'number',
                description: 'Number of results',
                default: 10,
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'get_top_headlines',
          description: 'Get top headlines',
          inputSchema: {
            type: 'object',
            properties: {
              category: {
                type: 'string',
                enum: ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'],
                description: 'News category',
              },
              country: {
                type: 'string',
                description: 'Country code (us, fr, gb, etc.)',
                default: 'us',
              },
              pageSize: {
                type: 'number',
                default: 10,
              },
            },
          },
        },
        {
          name: 'search_tech_news',
          description: 'Search for technology and science news',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              pageSize: {
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
              text: 'Error: NEWS_API_KEY not configured',
            },
          ],
        };
      }

      try {
        if (name === 'search_news') {
          return await this.searchNews(args);
        } else if (name === 'get_top_headlines') {
          return await this.getTopHeadlines(args);
        } else if (name === 'search_tech_news') {
          return await this.searchTechNews(args);
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

  private async searchNews(args: any) {
    const { query, language = 'en', sortBy = 'relevancy', pageSize = 10 } = args;

    const url = new URL(`${NEWS_API}/everything`);
    url.searchParams.append('q', query);
    url.searchParams.append('language', language);
    url.searchParams.append('sortBy', sortBy);
    url.searchParams.append('pageSize', pageSize.toString());
    url.searchParams.append('apiKey', this.apiKey!);

    const response = await fetch(url.toString());
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  private async getTopHeadlines(args: any) {
    const { category, country = 'us', pageSize = 10 } = args;

    const url = new URL(`${NEWS_API}/top-headlines`);
    if (category) url.searchParams.append('category', category);
    url.searchParams.append('country', country);
    url.searchParams.append('pageSize', pageSize.toString());
    url.searchParams.append('apiKey', this.apiKey!);

    const response = await fetch(url.toString());
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  private async searchTechNews(args: any) {
    const { query, pageSize = 10 } = args;

    const url = new URL(`${NEWS_API}/everything`);
    url.searchParams.append('q', query);
    url.searchParams.append('language', 'en');
    url.searchParams.append('sortBy', 'publishedAt');
    url.searchParams.append('pageSize', pageSize.toString());
    
    // Add tech/science domains
    const domains = 'techcrunch.com,wired.com,theverge.com,arstechnica.com,nature.com,sciencedaily.com';
    url.searchParams.append('domains', domains);
    url.searchParams.append('apiKey', this.apiKey!);

    const response = await fetch(url.toString());
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('News MCP Server running on stdio');
  }
}

const server = new NewsServer();
server.run().catch(console.error);


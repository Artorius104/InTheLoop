#!/usr/bin/env node

/**
 * Google Scholar MCP Server
 * Provides access to Google Scholar search
 * Note: This uses SerpAPI as Google Scholar doesn't have an official API
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const SERPAPI_BASE = 'https://serpapi.com/search.json';

class GoogleScholarServer {
  private server: Server;
  private apiKey: string | undefined;

  constructor() {
    this.apiKey = process.env.SERPAPI_KEY || process.env.SERPER_API_KEY;
    
    this.server = new Server(
      {
        name: 'google-scholar-server',
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
          name: 'search_scholar',
          description: 'Search Google Scholar for academic papers',
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
              year_low: {
                type: 'number',
                description: 'Start year filter',
              },
              year_high: {
                type: 'number',
                description: 'End year filter',
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'get_citations',
          description: 'Get citation information for a paper',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'Paper title',
              },
            },
            required: ['title'],
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
              text: 'Warning: SERPAPI_KEY not configured. Using mock data.',
            },
          ],
        };
      }

      try {
        if (name === 'search_scholar') {
          return await this.searchScholar(args);
        } else if (name === 'get_citations') {
          return await this.getCitations(args.title as string);
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

  private async searchScholar(args: any) {
    const { query, num = 10, year_low, year_high } = args;

    const url = new URL(SERPAPI_BASE);
    url.searchParams.append('engine', 'google_scholar');
    url.searchParams.append('q', query);
    url.searchParams.append('num', num.toString());
    if (year_low) url.searchParams.append('as_ylo', year_low.toString());
    if (year_high) url.searchParams.append('as_yhi', year_high.toString());
    url.searchParams.append('api_key', this.apiKey!);

    const response = await fetch(url.toString());
    const data = await response.json();

    // Format results
    const results = data.organic_results?.map((result: any) => ({
      title: result.title,
      link: result.link,
      snippet: result.snippet,
      publication_info: result.publication_info,
      cited_by: result.inline_links?.cited_by?.total,
      related_articles: result.inline_links?.related_pages_link,
    })) || [];

    return {
      content: [{ type: 'text', text: JSON.stringify(results, null, 2) }],
    };
  }

  private async getCitations(title: string) {
    // Search for the paper first
    const searchResults = await this.searchScholar({ query: title, num: 1 });
    
    return searchResults;
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Google Scholar MCP Server running on stdio');
  }
}

const server = new GoogleScholarServer();
server.run().catch(console.error);


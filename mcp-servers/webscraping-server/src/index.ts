#!/usr/bin/env node

/**
 * Web Scraping MCP Server
 * Provides web scraping capabilities
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';
import * as cheerio from 'cheerio';

class WebScrapingServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'webscraping-server',
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
          name: 'scrape_url',
          description: 'Scrape content from a URL',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'URL to scrape',
              },
              selector: {
                type: 'string',
                description: 'CSS selector for content (optional)',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'extract_text',
          description: 'Extract plain text from HTML',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'URL to extract text from',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'extract_links',
          description: 'Extract all links from a page',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'URL to extract links from',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'get_metadata',
          description: 'Extract metadata from a web page',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'URL to extract metadata from',
              },
            },
            required: ['url'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'scrape_url') {
          return await this.scrapeUrl(args.url as string, args.selector as string);
        } else if (name === 'extract_text') {
          return await this.extractText(args.url as string);
        } else if (name === 'extract_links') {
          return await this.extractLinks(args.url as string);
        } else if (name === 'get_metadata') {
          return await this.getMetadata(args.url as string);
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

  private async fetchHtml(url: string): Promise<string> {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; InTheLoop/1.0)',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.text();
  }

  private async scrapeUrl(url: string, selector?: string) {
    const html = await this.fetchHtml(url);
    const $ = cheerio.load(html);

    let content: string;
    if (selector) {
      content = $(selector).text();
    } else {
      content = $('body').text();
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            url,
            selector: selector || 'body',
            content: content.trim(),
          }, null, 2),
        },
      ],
    };
  }

  private async extractText(url: string) {
    const html = await this.fetchHtml(url);
    const $ = cheerio.load(html);

    // Remove script and style elements
    $('script, style').remove();

    const text = $('body').text()
      .replace(/\s+/g, ' ')
      .trim();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            url,
            text,
            length: text.length,
          }, null, 2),
        },
      ],
    };
  }

  private async extractLinks(url: string) {
    const html = await this.fetchHtml(url);
    const $ = cheerio.load(html);

    const links: Array<{ text: string; href: string }> = [];
    
    $('a[href]').each((_, element) => {
      const $el = $(element);
      const href = $el.attr('href');
      const text = $el.text().trim();
      
      if (href && text) {
        links.push({ text, href });
      }
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            url,
            linksCount: links.length,
            links: links.slice(0, 50), // Limit to 50 links
          }, null, 2),
        },
      ],
    };
  }

  private async getMetadata(url: string) {
    const html = await this.fetchHtml(url);
    const $ = cheerio.load(html);

    const metadata: Record<string, any> = {
      url,
      title: $('title').text(),
      description: $('meta[name="description"]').attr('content') || 
                   $('meta[property="og:description"]').attr('content'),
      image: $('meta[property="og:image"]').attr('content'),
      author: $('meta[name="author"]').attr('content'),
      publishedTime: $('meta[property="article:published_time"]').attr('content'),
      keywords: $('meta[name="keywords"]').attr('content'),
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(metadata, null, 2),
        },
      ],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Web Scraping MCP Server running on stdio');
  }
}

const server = new WebScrapingServer();
server.run().catch(console.error);


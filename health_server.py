#!/usr/bin/env python3
"""
Simple health check server for Railway deployment
"""
import asyncio
from aiohttp import web
import logging

logger = logging.getLogger(__name__)

async def health_check(request):
    """Health check endpoint"""
    return web.json_response({"status": "healthy", "service": "movie_bot"})

async def create_health_server():
    """Create a simple health check server"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    
    # Use port from environment or default to 8000
    import os
    port = int(os.environ.get('PORT', 8000))
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"Health server started on port {port}")
    return runner

async def run_health_server():
    """Run health server alongside the bot"""
    try:
        runner = await create_health_server()
        
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
            
    except Exception as e:
        logger.error(f"Health server error: {e}")
    finally:
        if 'runner' in locals():
            await runner.cleanup()
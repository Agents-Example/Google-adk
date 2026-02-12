"""
Main entry point for Google ADK Multi-Agent System.

This module provides the main entry point for running the multi-agent
system in various modes:
- Web UI mode (using App)
- CLI mode (using Runner)
- Interactive mode (for testing)

Usage:
    python main.py [--mode web|cli|interactive] [--port 8080]
"""

import asyncio
import argparse
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_web_mode(host: str = "localhost", port: int = 8080):
    """
    Run the multi-agent system with web UI.
    
    Starts the App with a web interface for interactive use.
    
    Args:
        host: Host to bind to.
        port: Port to listen on.
    """
    from app import create_app
    
    logger.info(f"Starting web UI on http://{host}:{port}")
    
    app = create_app()
    app.run(host=host, port=port)


async def run_cli_mode(message: str, user_id: str = "cli_user"):
    """
    Run a single message through the multi-agent system.
    
    Args:
        message: The message to process.
        user_id: User identifier.
    """
    from runner import create_runner, create_run_config
    
    logger.info(f"Processing message: {message[:50]}...")
    
    runner = create_runner()
    config = create_run_config(max_llm_calls=100)
    
    # Run agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=None,  # New session
        new_message=message,
        run_config=config,
    ):
        # Handle different event types
        if hasattr(event, 'content') and event.content:
            print(event.content)
        elif hasattr(event, 'type'):
            if event.type == "error":
                logger.error(f"Error: {event}")


async def run_interactive_mode(user_id: str = "interactive_user"):
    """
    Run an interactive chat session.
    
    Allows back-and-forth conversation with the multi-agent system.
    
    Args:
        user_id: User identifier.
    """
    from runner import create_runner, create_run_config
    
    logger.info("Starting interactive mode. Type 'quit' to exit.")
    
    runner = create_runner()
    config = create_run_config(max_llm_calls=100)
    session_id = None
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                logger.info("Exiting interactive mode.")
                break
            
            if not user_input:
                continue
            
            # Run agent
            print("\nAgent: ", end="", flush=True)
            
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_input,
                run_config=config,
            ):
                # Capture session ID for continuity
                if hasattr(event, 'session') and event.session:
                    session_id = event.session.id
                
                # Print content
                if hasattr(event, 'content') and event.content:
                    print(event.content, end="", flush=True)
            
            print()  # New line after response
            
        except KeyboardInterrupt:
            logger.info("\nInterrupted. Exiting.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")


async def demo_sequential_pipeline():
    """Demo: Run the sequential pipeline workflow."""
    from runner import create_inmemory_runner
    from agents.workflows.sequential import create_sequential_pipeline
    
    logger.info("Demo: Sequential Pipeline")
    
    pipeline = create_sequential_pipeline()
    runner = create_inmemory_runner(agent=pipeline)
    
    message = "Create a report on the current state of AI technology"
    logger.info(f"Input: {message}")
    
    async for event in runner.run_async(
        user_id="demo",
        session_id=None,
        new_message=message,
    ):
        if hasattr(event, 'content') and event.content:
            print(event.content)


async def demo_parallel_search():
    """Demo: Run the parallel search workflow."""
    from runner import create_inmemory_runner
    from agents.workflows.parallel import create_parallel_search
    
    logger.info("Demo: Parallel Search")
    
    parallel = create_parallel_search()
    runner = create_inmemory_runner(agent=parallel)
    
    message = "Find information about Python asyncio"
    logger.info(f"Input: {message}")
    
    async for event in runner.run_async(
        user_id="demo",
        session_id=None,
        new_message=message,
    ):
        if hasattr(event, 'content') and event.content:
            print(event.content)


async def demo_loop_refinement():
    """Demo: Run the loop refinement workflow."""
    from runner import create_inmemory_runner
    from agents.workflows.loop import create_loop_refinement
    
    logger.info("Demo: Loop Refinement")
    
    loop = create_loop_refinement(max_iterations=3)
    runner = create_inmemory_runner(agent=loop)
    
    message = "Improve this text: AI is good. It help people. Very useful."
    logger.info(f"Input: {message}")
    
    async for event in runner.run_async(
        user_id="demo",
        session_id=None,
        new_message=message,
    ):
        if hasattr(event, 'content') and event.content:
            print(event.content)


async def demo_full_system():
    """Demo: Run the full orchestrated multi-agent system."""
    from runner import create_runner
    from agents.orchestrator.agent import build_multi_agent_system
    
    logger.info("Demo: Full Multi-Agent System")
    
    agent = build_multi_agent_system()
    runner = create_runner(agent=agent)
    
    messages = [
        "Search for the latest news about AI",
        "Execute this Python code: print(2 + 2)",
        "What's the current time?",
    ]
    
    for message in messages:
        logger.info(f"\nInput: {message}")
        print("\nResponse: ", end="")
        
        async for event in runner.run_async(
            user_id="demo",
            session_id=None,
            new_message=message,
        ):
            if hasattr(event, 'content') and event.content:
                print(event.content, end="")
        
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Google ADK Multi-Agent System"
    )
    parser.add_argument(
        "--mode",
        choices=["web", "cli", "interactive", "demo"],
        default="interactive",
        help="Run mode (default: interactive)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for web mode (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for web mode (default: 8080)"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Message for CLI mode"
    )
    parser.add_argument(
        "--demo",
        choices=["sequential", "parallel", "loop", "full"],
        help="Demo to run in demo mode"
    )
    
    args = parser.parse_args()
    
    if args.mode == "web":
        run_web_mode(host=args.host, port=args.port)
    
    elif args.mode == "cli":
        if not args.message:
            parser.error("--message required for CLI mode")
        asyncio.run(run_cli_mode(args.message))
    
    elif args.mode == "interactive":
        asyncio.run(run_interactive_mode())
    
    elif args.mode == "demo":
        demo_map = {
            "sequential": demo_sequential_pipeline,
            "parallel": demo_parallel_search,
            "loop": demo_loop_refinement,
            "full": demo_full_system,
        }
        
        demo_name = args.demo or "full"
        if demo_name in demo_map:
            asyncio.run(demo_map[demo_name]())
        else:
            # Run all demos
            async def all_demos():
                await demo_sequential_pipeline()
                await demo_parallel_search()
                await demo_loop_refinement()
                await demo_full_system()
            
            asyncio.run(all_demos())


if __name__ == "__main__":
    main()

"""
Example: Using PentestAI with Kali MCP Server

Demonstrates how to:
1. Connect to Kali MCP server
2. Execute real pentest commands
3. Process results with LLM
"""

import os
from pentestai.core.config import PentestAIConfig
from pentestai.core.pentest_module import PlannerAgent, ExecutorAgent
from pentestai.mcp.client import KaliMCPClient


def main():
    # Setup configuration with MCP enabled
    config = PentestAIConfig(
        target="192.168.1.100",
        use_mcp=True,
        kali_mcp_url=os.getenv("KALI_MCP_URL", "http://localhost:5000"),
        sandbox_mode=False,  # Use real execution via MCP
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    print("=" * 70)
    print("PentestAI with Kali MCP Server - Example")
    print("=" * 70)
    
    # Step 1: Create MCP client and check connection
    print("\n[1] Connecting to Kali MCP Server...")
    mcp_client = KaliMCPClient(base_url=config.kali_mcp_url)
    
    if not mcp_client.health_check():
        print("❌ Failed to connect to Kali MCP Server!")
        print(f"   Make sure server is running at: {config.kali_mcp_url}")
        return
    
    print(f"✓ Connected to Kali MCP Server: {config.kali_mcp_url}")
    
    # Step 2: List available tools
    print("\n[2] Discovering available tools...")
    tools = mcp_client.list_tools()
    print(f"✓ Found {len(tools)} Kali tools:")
    
    # Group by category
    categories = {}
    for tool in tools:
        if tool.category not in categories:
            categories[tool.category] = []
        categories[tool.category].append(tool.name)
    
    for category, tool_names in sorted(categories.items()):
        print(f"   • {category}: {', '.join(tool_names)}")
    
    # Step 3: Get tool info
    print("\n[3] Getting nmap tool information...")
    nmap_info = mcp_client.get_tool_info("nmap")
    if nmap_info:
        print(f"   Name: {nmap_info.name}")
        print(f"   Description: {nmap_info.description}")
        print(f"   Usage: {nmap_info.usage}")
        print(f"   Example: {nmap_info.examples[0]}")
    
    # Step 4: Execute simple nmap command
    print(f"\n[4] Executing nmap scan on {config.target}...")
    print("   Command: nmap -sV -p 22,80,443 192.168.1.100")
    
    result = mcp_client.execute_command(
        tool="nmap",
        command=f"nmap -sV -p 22,80,443 {config.target}",
        timeout=60
    )
    
    print(f"\n   Result:")
    print(f"   Success: {result.success}")
    print(f"   Exit Code: {result.exit_code}")
    print(f"   Execution Time: {result.execution_time:.2f}s")
    print(f"\n   Output:")
    print("   " + "\n   ".join(result.stdout.split("\n")[:20]))  # First 20 lines
    
    if result.stderr:
        print(f"\n   Errors: {result.stderr}")
    
    # Step 5: Create ExecutorAgent with MCP
    print("\n[5] Creating ExecutorAgent with MCP integration...")
    executor = ExecutorAgent(config=config, mcp_client=mcp_client)
    
    available_tools = executor.get_available_tools()
    print(f"✓ ExecutorAgent ready with {len(available_tools)} tools")
    
    # Step 6: Get tool suggestions for a task
    print("\n[6] Getting tool suggestions for 'web vulnerability scanning'...")
    suggestions = executor.get_tool_suggestions("scan web server for vulnerabilities")
    
    if suggestions:
        print(f"✓ Found {len(suggestions)} suggested tools:")
        for tool in suggestions[:5]:  # Show top 5
            print(f"   • {tool['name']}: {tool['description']}")
            print(f"     Example: {tool['examples'][0]}")
    
    # Step 7: Create attack plan with Planner
    print(f"\n[7] Creating attack plan for target {config.target}...")
    planner = PlannerAgent(config=config)
    attack_plan = planner.create_initial_plan(target=config.target)
    
    print(f"✓ Attack plan created with {len(attack_plan.subtasks)} phases")
    
    # Step 8: Execute first task with MCP
    print("\n[8] Executing first task from attack plan...")
    first_task = planner.get_next_task()
    
    if first_task:
        print(f"   Task: {first_task.description}")
        print(f"   Command: {first_task.command}")
        
        # This will use MCP automatically since executor has mcp_client
        execution_result = executor.execute_task(first_task)
        
        print(f"\n   Execution Result:")
        print(f"   Success: {execution_result.success}")
        print(f"   Vulnerabilities Found: {len(execution_result.vulnerabilities_found)}")
        
        if execution_result.vulnerabilities_found:
            print(f"\n   Vulnerabilities:")
            for vuln in execution_result.vulnerabilities_found:
                print(f"   • {vuln}")
        
        # Show output preview
        output_lines = execution_result.output.split("\n")
        print(f"\n   Output Preview (first 10 lines):")
        for line in output_lines[:10]:
            print(f"   {line}")
    
    # Cleanup
    print("\n[9] Closing MCP connection...")
    mcp_client.close()
    print("✓ Done!")
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    
    print("\nNext Steps:")
    print("1. Review the output and vulnerabilities found")
    print("2. Run full assessment: python -m pentestai.cli --target 192.168.1.100 --mode full")
    print("3. Use interactive CLI: python pentestai_interactive.py")
    print("4. Check MCP API docs: http://localhost:5000/docs")


if __name__ == "__main__":
    main()

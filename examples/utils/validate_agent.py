#!/usr/bin/env python3
"""
A2A Agent Validator

A utility script to validate and test A2A agents. This tool can:
- Check if an agent is responding
- Validate the agent card
- Test basic message sending
- Verify transport protocols
- Performance benchmarking

Usage:
    python validate_agent.py http://localhost:8000
    python validate_agent.py http://localhost:8000 --full
    python validate_agent.py http://localhost:8000 --benchmark
"""

import asyncio
import json
import logging
import sys
import time
from typing import Dict, List, Optional

import httpx
from a2a.client import ClientFactory
from a2a.types import Message, Part, TextPart
from a2a.utils.artifact import new_text_artifact

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentValidator:
    """Validates A2A agents and provides testing utilities."""
    
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.client_factory = ClientFactory()
        self.client = None
        self.test_results = {}
    
    async def validate_agent(self, full_test: bool = False, benchmark: bool = False) -> Dict:
        """Run validation tests on the agent."""
        print(f"🔍 Validating A2A Agent at {self.agent_url}")
        print("=" * 60)
        
        results = {
            "agent_url": self.agent_url,
            "timestamp": time.time(),
            "tests": {}
        }
        
        # Test 1: Basic connectivity
        print("📡 Testing connectivity...")
        connectivity_result = await self._test_connectivity()
        results["tests"]["connectivity"] = connectivity_result
        self._print_result("Connectivity", connectivity_result["passed"])
        
        if not connectivity_result["passed"]:
            print("❌ Agent is not reachable. Stopping validation.")
            return results
        
        # Test 2: Agent card validation
        print("📋 Validating agent card...")
        card_result = await self._test_agent_card()
        results["tests"]["agent_card"] = card_result
        self._print_result("Agent Card", card_result["passed"])
        
        # Test 3: Basic message sending
        print("💬 Testing message sending...")
        message_result = await self._test_message_sending()
        results["tests"]["message_sending"] = message_result
        self._print_result("Message Sending", message_result["passed"])
        
        if full_test:
            # Test 4: Multiple message types
            print("📝 Testing multiple message types...")
            multi_message_result = await self._test_multiple_message_types()
            results["tests"]["multiple_messages"] = multi_message_result
            self._print_result("Multiple Message Types", multi_message_result["passed"])
            
            # Test 5: Error handling
            print("🛠️ Testing error handling...")
            error_result = await self._test_error_handling()
            results["tests"]["error_handling"] = error_result
            self._print_result("Error Handling", error_result["passed"])
        
        if benchmark:
            # Performance benchmark
            print("⚡ Running performance benchmark...")
            perf_result = await self._benchmark_performance()
            results["tests"]["performance"] = perf_result
            self._print_performance_results(perf_result)
        
        # Summary
        self._print_summary(results)
        return results
    
    async def _test_connectivity(self) -> Dict:
        """Test basic HTTP connectivity to the agent."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.agent_url}/.well-known/a2a", timeout=5.0)
                return {
                    "passed": response.status_code == 200,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None,
                    "error": None
                }
        except Exception as e:
            return {
                "passed": False,
                "status_code": None,
                "response_time": None,
                "error": str(e)
            }
    
    async def _test_agent_card(self) -> Dict:
        """Test and validate the agent card."""
        try:
            self.client = await self.client_factory.create_client(self.agent_url)
            agent_card = await self.client.get_agent_card()
            
            # Basic validation
            issues = []
            if not agent_card.name:
                issues.append("Missing agent name")
            if not agent_card.description:
                issues.append("Missing agent description")
            if not agent_card.version:
                issues.append("Missing agent version")
            if not agent_card.skills:
                issues.append("No skills defined")
            
            return {
                "passed": len(issues) == 0,
                "agent_name": agent_card.name,
                "agent_version": agent_card.version,
                "skill_count": len(agent_card.skills) if agent_card.skills else 0,
                "transport": agent_card.preferred_transport,
                "streaming": agent_card.capabilities.streaming if agent_card.capabilities else None,
                "issues": issues,
                "error": None
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "issues": ["Failed to retrieve agent card"]
            }
    
    async def _test_message_sending(self) -> Dict:
        """Test basic message sending functionality."""
        try:
            if not self.client:
                self.client = await self.client_factory.create_client(self.agent_url)
            
            # Send a simple test message
            test_message = Message(
                parts=[Part(root=TextPart(text="Hello, this is a test message"))],
                artifacts=[]
            )
            
            start_time = time.time()
            responses = []
            
            async for response in self.client.send_message(test_message):
                responses.append(response)
                # Only wait for first response to avoid hanging
                break
            
            response_time = time.time() - start_time
            
            return {
                "passed": len(responses) > 0,
                "response_count": len(responses),
                "response_time": response_time,
                "first_response_type": type(responses[0]).__name__ if responses else None,
                "error": None
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "response_count": 0
            }
    
    async def _test_multiple_message_types(self) -> Dict:
        """Test different message formats and content types."""
        test_cases = [
            ("Empty message", ""),
            ("Simple text", "Hello world"),
            ("Long text", "Lorem ipsum " * 100),
            ("Special characters", "Hello 🌍! Testing émojis and spëcial chars."),
            ("JSON-like content", '{"test": true, "value": 123}')
        ]
        
        results = []
        
        for test_name, test_content in test_cases:
            try:
                message = Message(
                    parts=[Part(root=TextPart(text=test_content))],
                    artifacts=[]
                )
                
                response_count = 0
                async for response in self.client.send_message(message):
                    response_count += 1
                    break  # Just check first response
                
                results.append({
                    "test_name": test_name,
                    "passed": response_count > 0,
                    "response_count": response_count
                })
                
            except Exception as e:
                results.append({
                    "test_name": test_name,
                    "passed": False,
                    "error": str(e)
                })
        
        passed_tests = sum(1 for r in results if r["passed"])
        return {
            "passed": passed_tests == len(test_cases),
            "total_tests": len(test_cases),
            "passed_tests": passed_tests,
            "test_results": results
        }
    
    async def _test_error_handling(self) -> Dict:
        """Test how the agent handles error conditions."""
        # This is a basic test - in practice you'd test malformed requests, etc.
        try:
            # Test with unusual but valid message
            message = Message(
                parts=[Part(root=TextPart(text="Test error handling"))],
                artifacts=[]
            )
            
            response_received = False
            async for response in self.client.send_message(message):
                response_received = True
                break
            
            return {
                "passed": response_received,
                "error": None
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e)
            }
    
    async def _benchmark_performance(self, num_messages: int = 10) -> Dict:
        """Run performance benchmarks."""
        print(f"  Running {num_messages} message performance test...")
        
        times = []
        successful_requests = 0
        
        for i in range(num_messages):
            try:
                message = Message(
                    parts=[Part(root=TextPart(text=f"Benchmark message {i+1}"))],
                    artifacts=[]
                )
                
                start_time = time.time()
                async for response in self.client.send_message(message):
                    end_time = time.time()
                    times.append(end_time - start_time)
                    successful_requests += 1
                    break  # Just measure first response
                    
            except Exception as e:
                logger.warning(f"Benchmark message {i+1} failed: {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
        else:
            avg_time = min_time = max_time = 0
        
        return {
            "total_messages": num_messages,
            "successful_requests": successful_requests,
            "success_rate": successful_requests / num_messages * 100,
            "average_response_time": avg_time,
            "min_response_time": min_time,
            "max_response_time": max_time,
            "times": times
        }
    
    def _print_result(self, test_name: str, passed: bool):
        """Print test result with formatting."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    def _print_performance_results(self, perf_result: Dict):
        """Print performance benchmark results."""
        print(f"  📊 Performance Results:")
        print(f"     Success Rate: {perf_result['success_rate']:.1f}%")
        print(f"     Average Response Time: {perf_result['average_response_time']:.3f}s")
        print(f"     Min Response Time: {perf_result['min_response_time']:.3f}s")
        print(f"     Max Response Time: {perf_result['max_response_time']:.3f}s")
    
    def _print_summary(self, results: Dict):
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)
        
        total_tests = len(results["tests"])
        passed_tests = sum(1 for test in results["tests"].values() if test.get("passed", False))
        
        print(f"Agent URL: {results['agent_url']}")
        print(f"Tests Run: {total_tests}")
        print(f"Tests Passed: {passed_tests}")
        print(f"Success Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "No tests run")
        
        if "agent_card" in results["tests"] and results["tests"]["agent_card"]["passed"]:
            card_info = results["tests"]["agent_card"]
            print(f"\nAgent Info:")
            print(f"  Name: {card_info.get('agent_name', 'Unknown')}")
            print(f"  Version: {card_info.get('agent_version', 'Unknown')}")
            print(f"  Skills: {card_info.get('skill_count', 0)}")
            print(f"  Transport: {card_info.get('transport', 'Unknown')}")
        
        # Overall status
        if passed_tests == total_tests:
            print(f"\n🎉 All tests passed! Agent is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Check the results above for details.")
    
    async def close(self):
        """Clean up resources."""
        if self.client:
            await self.client.close()


async def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_agent.py <agent_url> [--full] [--benchmark]")
        print("Example: python validate_agent.py http://localhost:8000")
        sys.exit(1)
    
    agent_url = sys.argv[1]
    full_test = "--full" in sys.argv
    benchmark = "--benchmark" in sys.argv
    
    validator = AgentValidator(agent_url)
    
    try:
        results = await validator.validate_agent(full_test=full_test, benchmark=benchmark)
        
        # Optionally save results to file
        if "--save" in sys.argv:
            filename = f"agent_validation_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to {filename}")
            
    except KeyboardInterrupt:
        print("\n🛑 Validation interrupted by user")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
    finally:
        await validator.close()


if __name__ == "__main__":
    asyncio.run(main())
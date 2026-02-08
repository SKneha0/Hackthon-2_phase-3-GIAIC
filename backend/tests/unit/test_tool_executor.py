import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.tool_executor import ToolExecutor


@pytest.fixture
def tool_executor():
    """Create a ToolExecutor instance for testing"""
    executor = ToolExecutor()
    return executor


@pytest.mark.asyncio
async def test_execute_tool_success(tool_executor):
    """Test successful tool execution"""
    # Mock a simple tool function
    mock_tool = AsyncMock(return_value={"result": "success"})
    tool_executor.tools = {"test_tool": mock_tool}
    
    # Execute the tool
    result = await tool_executor.execute_tool("test_tool", {"param": "value"}, "user123")
    
    # Assertions
    assert result == {"result": "success"}
    mock_tool.assert_called_once_with(param="value", user_id="user123")


@pytest.mark.asyncio
async def test_execute_tool_not_found(tool_executor):
    """Test execution of non-existent tool"""
    with pytest.raises(ValueError) as exc_info:
        await tool_executor.execute_tool("nonexistent_tool", {}, "user123")
    
    assert "not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_execute_tool_validation_error(tool_executor):
    """Test tool execution with validation error"""
    # Create a tool that raises a ValueError
    async def validation_error_tool(**kwargs):
        raise ValueError("Invalid parameter")
    
    tool_executor.tools = {"validation_error_tool": validation_error_tool}
    
    with pytest.raises(ValueError) as exc_info:
        await tool_executor.execute_tool("validation_error_tool", {"param": "value"}, "user123")
    
    assert "Validation error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_execute_tool_permission_error(tool_executor):
    """Test tool execution with permission error"""
    # Create a tool that raises a PermissionError
    async def permission_error_tool(**kwargs):
        raise PermissionError("Access denied")
    
    tool_executor.tools = {"permission_error_tool": permission_error_tool}
    
    with pytest.raises(PermissionError) as exc_info:
        await tool_executor.execute_tool("permission_error_tool", {"param": "value"}, "user123")
    
    assert "Permission error" in str(exc_info.value)


def test_get_tool_schema(tool_executor):
    """Test getting tool schema"""
    schema = tool_executor.get_tool_schema("add_task")
    assert schema is not None
    assert "name" in schema
    assert schema["name"] == "add_task"
"""
Tests for UNIMIND LVX Orchestration System Configuration
"""

import json
import os
import pytest
from pathlib import Path


# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
ORCHESTRATION_ROOT = PROJECT_ROOT / "orchestration"
MODELS_ROOT = PROJECT_ROOT / "models"


class TestConfigurationFiles:
    """Test configuration files are valid and well-formed"""

    def test_cognitive_plugins_exists(self):
        """Test that cognitive_plugins.txt exists"""
        plugins_file = ORCHESTRATION_ROOT / "config" / "cognitive_plugins.txt"
        assert plugins_file.exists(), "cognitive_plugins.txt should exist"

    def test_cognitive_plugins_format(self):
        """Test that cognitive_plugins.txt has valid format"""
        plugins_file = ORCHESTRATION_ROOT / "config" / "cognitive_plugins.txt"
        
        with open(plugins_file, 'r') as f:
            lines = f.readlines()
        
        # Filter out comments and empty lines
        data_lines = [line.strip() for line in lines 
                      if line.strip() and not line.strip().startswith('#')]
        
        assert len(data_lines) > 0, "Should have at least one plugin entry"
        
        # Check format: plugin_id|plugin_name|version|capabilities|dependencies
        for line in data_lines:
            parts = line.split('|')
            assert len(parts) == 5, f"Plugin line should have 5 fields: {line}"
            assert parts[0], "Plugin ID should not be empty"
            assert parts[1], "Plugin name should not be empty"
            assert parts[2], "Version should not be empty"

    def test_affiliate_config_json_valid(self):
        """Test that affiliate_config.json is valid JSON"""
        config_file = ORCHESTRATION_ROOT / "config" / "affiliate_config.json"
        assert config_file.exists(), "affiliate_config.json should exist"
        
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert "version" in data, "Should have version field"
        assert "affiliate_system" in data, "Should have affiliate_system config"
        assert "platforms" in data, "Should have platforms list"
        assert isinstance(data["platforms"], list), "Platforms should be a list"

    def test_affiliate_config_structure(self):
        """Test affiliate_config.json has required structure"""
        config_file = ORCHESTRATION_ROOT / "config" / "affiliate_config.json"
        
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        # Check main sections
        required_sections = ["version", "affiliate_system", "platforms", 
                           "tracking", "compliance", "analytics"]
        for section in required_sections:
            assert section in data, f"Should have {section} section"
        
        # Check platform structure
        if data["platforms"]:
            platform = data["platforms"][0]
            assert "id" in platform, "Platform should have ID"
            assert "name" in platform, "Platform should have name"
            assert "enabled" in platform, "Platform should have enabled flag"

    def test_workspace_guidance_json_valid(self):
        """Test that workspace_guidance.json is valid JSON"""
        config_file = ORCHESTRATION_ROOT / "config" / "workspace_guidance.json"
        assert config_file.exists(), "workspace_guidance.json should exist"
        
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert "version" in data, "Should have version field"
        assert "workspace_guidance_system" in data, "Should have workspace_guidance_system config"
        assert "tutorials" in data, "Should have tutorials list"
        assert isinstance(data["tutorials"], list), "Tutorials should be a list"

    def test_workspace_guidance_structure(self):
        """Test workspace_guidance.json has required structure"""
        config_file = ORCHESTRATION_ROOT / "config" / "workspace_guidance.json"
        
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        # Check main sections
        required_sections = ["version", "workspace_guidance_system", "tutorials", 
                           "contextual_help", "role_guidance"]
        for section in required_sections:
            assert section in data, f"Should have {section} section"
        
        # Check tutorial structure
        if data["tutorials"]:
            tutorial = data["tutorials"][0]
            assert "id" in tutorial, "Tutorial should have ID"
            assert "title" in tutorial, "Tutorial should have title"
            assert "difficulty" in tutorial, "Tutorial should have difficulty"
            assert "steps" in tutorial, "Tutorial should have steps"
            assert isinstance(tutorial["steps"], list), "Steps should be a list"

    def test_baseline_manifest_exists(self):
        """Test that baseline_manifest.sha256 exists"""
        manifest_file = ORCHESTRATION_ROOT / "config" / "baseline_manifest.sha256"
        assert manifest_file.exists(), "baseline_manifest.sha256 should exist"


class TestPersonaFiles:
    """Test persona JSON files are valid"""

    def test_atlas_architect_persona_valid(self):
        """Test atlas_architect.json is valid JSON"""
        persona_file = MODELS_ROOT / "personas" / "atlas_architect.json"
        assert persona_file.exists(), "atlas_architect.json should exist"
        
        with open(persona_file, 'r') as f:
            data = json.load(f)
        
        assert "persona_metadata" in data, "Should have persona_metadata"
        assert "core_identity" in data, "Should have core_identity"
        assert "capabilities" in data, "Should have capabilities"
        assert "safety_metadata" in data, "Should have safety_metadata"

    def test_legion_x_controller_persona_valid(self):
        """Test legion_x_controller.json is valid JSON"""
        persona_file = MODELS_ROOT / "personas" / "legion_x_controller.json"
        assert persona_file.exists(), "legion_x_controller.json should exist"
        
        with open(persona_file, 'r') as f:
            data = json.load(f)
        
        assert "persona_metadata" in data, "Should have persona_metadata"
        assert "core_identity" in data, "Should have core_identity"
        assert "capabilities" in data, "Should have capabilities"
        assert "safety_metadata" in data, "Should have safety_metadata"

    def test_persona_metadata_structure(self):
        """Test all personas have required metadata structure"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        assert len(persona_files) >= 2, "Should have at least 2 personas"
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            # Check metadata
            assert "persona_metadata" in data
            metadata = data["persona_metadata"]
            assert "id" in metadata, f"{persona_file.name} should have id"
            assert "name" in metadata, f"{persona_file.name} should have name"
            assert "version" in metadata, f"{persona_file.name} should have version"
            assert "description" in metadata, f"{persona_file.name} should have description"

    def test_persona_safety_metadata(self):
        """Test all personas have safety metadata"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            assert "safety_metadata" in data, f"{persona_file.name} should have safety_metadata"
            safety = data["safety_metadata"]
            
            assert "safety_level" in safety, f"{persona_file.name} should have safety_level"
            assert "constraints" in safety, f"{persona_file.name} should have constraints"
            assert isinstance(safety["constraints"], list), "Constraints should be a list"
            assert len(safety["constraints"]) > 0, "Should have at least one constraint"

    def test_persona_capabilities_structure(self):
        """Test all personas have proper capabilities structure"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            assert "capabilities" in data, f"{persona_file.name} should have capabilities"
            capabilities = data["capabilities"]
            
            assert "primary_functions" in capabilities, "Should have primary_functions"
            assert "cognitive_plugins" in capabilities, "Should have cognitive_plugins"
            assert "panel_awareness" in capabilities, "Should have panel_awareness"

    def test_persona_panel_awareness(self):
        """Test personas have panel awareness configuration"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            panel_awareness = data["capabilities"]["panel_awareness"]
            
            assert "primary_panel" in panel_awareness, "Should have primary_panel"
            assert "monitors" in panel_awareness, "Should have monitors"
            assert "logs_to" in panel_awareness, "Should have logs_to"
            assert isinstance(panel_awareness["monitors"], list), "Monitors should be a list"
            assert isinstance(panel_awareness["logs_to"], list), "Logs_to should be a list"

    def test_persona_affiliate_tasks(self):
        """Test personas have affiliate tasks configuration"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            assert "affiliate_tasks" in data, f"{persona_file.name} should have affiliate_tasks"
            affiliate = data["affiliate_tasks"]
            
            assert "enabled" in affiliate, "Should have enabled flag"
            assert "responsibilities" in affiliate, "Should have responsibilities"
            assert "promotion_strategy" in affiliate, "Should have promotion_strategy"

    def test_persona_workspace_guidance(self):
        """Test personas have workspace guidance configuration"""
        personas_dir = MODELS_ROOT / "personas"
        persona_files = list(personas_dir.glob("*.json"))
        
        for persona_file in persona_files:
            with open(persona_file, 'r') as f:
                data = json.load(f)
            
            assert "workspace_guidance" in data, f"{persona_file.name} should have workspace_guidance"
            guidance = data["workspace_guidance"]
            
            assert "role" in guidance, "Should have role"
            assert "recommended_tutorials" in guidance, "Should have recommended_tutorials"


class TestOrchestrationScripts:
    """Test orchestration script files exist"""

    def test_main_bat_script_exists(self):
        """Test main orchestration script exists"""
        script_file = ORCHESTRATION_ROOT / "bat" / "unimind_lvx_master.bat"
        assert script_file.exists(), "unimind_lvx_master.bat should exist"

    def test_stage_script_exists(self):
        """Test multi-stage orchestration script exists"""
        script_file = ORCHESTRATION_ROOT / "bat" / "unimind_lvx_master_stage_1_9_final.bat"
        assert script_file.exists(), "unimind_lvx_master_stage_1_9_final.bat should exist"

    def test_helper_scripts_exist(self):
        """Test all helper scripts exist"""
        helpers = [
            "logger.bat",
            "error_handler.bat",
            "manifest_validator.bat",
            "directory_setup.bat",
            "session_context.bat",
            "verify_manifest.ps1",
            "setup_directories.ps1"
        ]
        
        for helper in helpers:
            helper_file = ORCHESTRATION_ROOT / "helpers" / helper
            assert helper_file.exists(), f"{helper} should exist"

    def test_documentation_exists(self):
        """Test orchestration README exists"""
        readme_file = ORCHESTRATION_ROOT / "README.md"
        assert readme_file.exists(), "orchestration/README.md should exist"
        
        # Check it has content
        with open(readme_file, 'r') as f:
            content = f.read()
        
        assert len(content) > 1000, "README should have substantial content"
        assert "UNIMIND LVX" in content, "README should mention UNIMIND LVX"
        assert "Legion-X" in content, "README should mention Legion-X"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

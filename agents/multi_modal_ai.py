"""
Multi-Modal AI Integration
===========================
Integrates multiple AI capabilities:
- Text understanding and generation
- Code analysis and generation  
- Vision processing
- Audio processing
- Cross-modal reasoning
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
import base64


class Modality(Enum):
    """Supported modalities"""
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    STRUCTURED_DATA = "structured_data"


@dataclass
class ModalInput:
    """Multi-modal input structure"""
    modality: Modality
    content: Any
    metadata: Dict[str, Any]


@dataclass
class ModalOutput:
    """Multi-modal output structure"""
    modality: Modality
    content: Any
    confidence: float
    metadata: Dict[str, Any]


class MultiModalAI:
    """
    Multi-modal AI system capable of processing and generating
    content across different modalities
    """
    
    def __init__(self):
        self.supported_modalities = [m.value for m in Modality]
        self.cross_modal_cache = {}
        
    def process(self, inputs: List[ModalInput]) -> List[ModalOutput]:
        """
        Process multi-modal inputs
        
        Args:
            inputs: List of modal inputs
            
        Returns:
            List of processed outputs
        """
        outputs = []
        
        for modal_input in inputs:
            if modal_input.modality == Modality.TEXT:
                output = self._process_text(modal_input)
            elif modal_input.modality == Modality.CODE:
                output = self._process_code(modal_input)
            elif modal_input.modality == Modality.IMAGE:
                output = self._process_image(modal_input)
            elif modal_input.modality == Modality.AUDIO:
                output = self._process_audio(modal_input)
            elif modal_input.modality == Modality.STRUCTURED_DATA:
                output = self._process_structured_data(modal_input)
            else:
                output = ModalOutput(
                    modality=modal_input.modality,
                    content=f"Unsupported modality: {modal_input.modality}",
                    confidence=0.0,
                    metadata={"error": "unsupported_modality"}
                )
            
            outputs.append(output)
        
        return outputs
    
    def _process_text(self, input_data: ModalInput) -> ModalOutput:
        """Process text input"""
        text = input_data.content
        
        analysis = {
            "length": len(text),
            "word_count": len(text.split()),
            "sentiment": self._analyze_sentiment(text),
            "entities": self._extract_entities(text),
            "key_concepts": self._extract_concepts(text),
            "language": "en",
            "complexity": self._assess_complexity(text)
        }
        
        return ModalOutput(
            modality=Modality.TEXT,
            content=analysis,
            confidence=0.9,
            metadata={"processing_method": "nlp_analysis"}
        )
    
    def _process_code(self, input_data: ModalInput) -> ModalOutput:
        """Process code input"""
        code = input_data.content
        
        analysis = {
            "language": self._detect_language(code),
            "lines_of_code": len(code.split('\n')),
            "functions": self._extract_functions(code),
            "classes": self._extract_classes(code),
            "imports": self._extract_imports(code),
            "complexity_score": self._calculate_code_complexity(code),
            "issues": self._detect_code_issues(code),
            "suggestions": self._generate_code_suggestions(code)
        }
        
        return ModalOutput(
            modality=Modality.CODE,
            content=analysis,
            confidence=0.85,
            metadata={"processing_method": "static_analysis"}
        )
    
    def _process_image(self, input_data: ModalInput) -> ModalOutput:
        """Process image input"""
        # Simulated image processing
        image_data = input_data.content
        
        analysis = {
            "format": input_data.metadata.get("format", "unknown"),
            "dimensions": input_data.metadata.get("dimensions", "unknown"),
            "objects_detected": [
                {"object": "simulated_object", "confidence": 0.85, "bbox": [0, 0, 100, 100]}
            ],
            "scene_description": "Simulated scene analysis",
            "dominant_colors": ["#FF0000", "#00FF00", "#0000FF"],
            "text_in_image": []
        }
        
        return ModalOutput(
            modality=Modality.IMAGE,
            content=analysis,
            confidence=0.75,
            metadata={"processing_method": "computer_vision"}
        )
    
    def _process_audio(self, input_data: ModalInput) -> ModalOutput:
        """Process audio input"""
        # Simulated audio processing
        audio_data = input_data.content
        
        analysis = {
            "duration": input_data.metadata.get("duration", "unknown"),
            "format": input_data.metadata.get("format", "unknown"),
            "transcript": "Simulated audio transcription",
            "speaker_count": 1,
            "language": "en",
            "sentiment": "neutral",
            "key_phrases": ["example phrase 1", "example phrase 2"]
        }
        
        return ModalOutput(
            modality=Modality.AUDIO,
            content=analysis,
            confidence=0.8,
            metadata={"processing_method": "speech_recognition"}
        )
    
    def _process_structured_data(self, input_data: ModalInput) -> ModalOutput:
        """Process structured data (JSON, CSV, etc.)"""
        data = input_data.content
        
        analysis = {
            "type": type(data).__name__,
            "schema": self._infer_schema(data),
            "statistics": self._compute_statistics(data),
            "patterns": self._detect_patterns(data),
            "quality_score": 0.85,
            "anomalies": []
        }
        
        return ModalOutput(
            modality=Modality.STRUCTURED_DATA,
            content=analysis,
            confidence=0.9,
            metadata={"processing_method": "data_analysis"}
        )
    
    # Helper methods for text processing
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze text sentiment"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'poor', 'horrible']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities"""
        # Simplified entity extraction
        return [
            {"entity": "example_entity", "type": "ORGANIZATION", "confidence": 0.8}
        ]
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts"""
        words = text.lower().split()
        # Filter common words and return unique
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        concepts = [w for w in set(words) if len(w) > 4 and w not in stopwords]
        return concepts[:10]
    
    def _assess_complexity(self, text: str) -> str:
        """Assess text complexity"""
        avg_word_length = sum(len(word) for word in text.split()) / max(len(text.split()), 1)
        
        if avg_word_length > 7:
            return "high"
        elif avg_word_length > 5:
            return "medium"
        else:
            return "low"
    
    # Helper methods for code processing
    def _detect_language(self, code: str) -> str:
        """Detect programming language"""
        if 'def ' in code and 'import ' in code:
            return "python"
        elif 'function' in code and 'const' in code:
            return "javascript"
        elif 'public class' in code:
            return "java"
        elif '#include' in code:
            return "c++"
        else:
            return "unknown"
    
    def _extract_functions(self, code: str) -> List[str]:
        """Extract function names"""
        functions = []
        for line in code.split('\n'):
            if 'def ' in line:
                # Python function
                parts = line.split('def ')[1].split('(')[0].strip()
                functions.append(parts)
            elif 'function ' in line:
                # JavaScript function
                parts = line.split('function ')[1].split('(')[0].strip()
                functions.append(parts)
        return functions
    
    def _extract_classes(self, code: str) -> List[str]:
        """Extract class names"""
        classes = []
        for line in code.split('\n'):
            if 'class ' in line:
                parts = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                classes.append(parts)
        return classes
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract import statements"""
        imports = []
        for line in code.split('\n'):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                imports.append(line.strip())
        return imports
    
    def _calculate_code_complexity(self, code: str) -> float:
        """Calculate code complexity score"""
        lines = code.split('\n')
        complexity = len(lines) * 0.1
        
        # Add complexity for control structures
        complexity += code.count('if ') * 0.2
        complexity += code.count('for ') * 0.3
        complexity += code.count('while ') * 0.3
        complexity += code.count('try:') * 0.5
        
        return min(complexity, 10.0)
    
    def _detect_code_issues(self, code: str) -> List[Dict[str, str]]:
        """Detect potential code issues"""
        issues = []
        
        if 'eval(' in code:
            issues.append({"severity": "high", "issue": "Use of eval() detected", "line": 0})
        
        if code.count('\t') > 0 and code.count('    ') > 0:
            issues.append({"severity": "low", "issue": "Mixed tabs and spaces", "line": 0})
        
        return issues
    
    def _generate_code_suggestions(self, code: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if 'def ' in code and '"""' not in code and "'''" not in code:
            suggestions.append("Add docstrings to functions")
        
        if code.count('\n') > 50:
            suggestions.append("Consider breaking into smaller functions")
        
        if 'import *' in code:
            suggestions.append("Avoid wildcard imports")
        
        return suggestions
    
    # Helper methods for data processing
    def _infer_schema(self, data: Any) -> Dict[str, str]:
        """Infer data schema"""
        if isinstance(data, dict):
            return {k: type(v).__name__ for k, v in data.items()}
        elif isinstance(data, list) and data:
            return {"type": "array", "element_type": type(data[0]).__name__}
        else:
            return {"type": type(data).__name__}
    
    def _compute_statistics(self, data: Any) -> Dict[str, Any]:
        """Compute data statistics"""
        if isinstance(data, list):
            return {
                "count": len(data),
                "sample": data[:3] if len(data) > 3 else data
            }
        elif isinstance(data, dict):
            return {
                "keys": len(data.keys()),
                "sample_keys": list(data.keys())[:5]
            }
        else:
            return {"type": type(data).__name__}
    
    def _detect_patterns(self, data: Any) -> List[str]:
        """Detect patterns in data"""
        patterns = []
        
        if isinstance(data, dict):
            if all(isinstance(v, (int, float)) for v in data.values()):
                patterns.append("All numeric values")
            if all(isinstance(v, str) for v in data.values()):
                patterns.append("All string values")
        
        return patterns
    
    def cross_modal_reasoning(self, inputs: List[ModalInput]) -> Dict[str, Any]:
        """
        Perform reasoning across multiple modalities
        
        Args:
            inputs: List of inputs from different modalities
            
        Returns:
            Cross-modal analysis
        """
        modalities = [inp.modality.value for inp in inputs]
        
        synthesis = {
            "input_modalities": modalities,
            "cross_modal_insights": [],
            "unified_understanding": "",
            "confidence": 0.75
        }
        
        # Example cross-modal reasoning
        if Modality.TEXT.value in modalities and Modality.CODE.value in modalities:
            synthesis["cross_modal_insights"].append(
                "Text description aligns with code implementation"
            )
        
        if Modality.IMAGE.value in modalities and Modality.TEXT.value in modalities:
            synthesis["cross_modal_insights"].append(
                "Visual content correlates with textual description"
            )
        
        synthesis["unified_understanding"] = f"Synthesized understanding from {len(modalities)} modalities"
        
        return synthesis


if __name__ == "__main__":
    print("=" * 70)
    print("MULTI-MODAL AI - Demo")
    print("=" * 70)
    
    mmai = MultiModalAI()
    
    # Demo 1: Text processing
    print("\n[1] Text Processing:")
    text_input = ModalInput(
        modality=Modality.TEXT,
        content="This is an excellent example of multi-modal AI processing capabilities.",
        metadata={}
    )
    text_output = mmai.process([text_input])[0]
    print(f"   Sentiment: {text_output.content['sentiment']}")
    print(f"   Complexity: {text_output.content['complexity']}")
    print(f"   Confidence: {text_output.confidence:.2%}")
    
    # Demo 2: Code processing
    print("\n[2] Code Processing:")
    code_sample = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""
    code_input = ModalInput(
        modality=Modality.CODE,
        content=code_sample,
        metadata={}
    )
    code_output = mmai.process([code_input])[0]
    print(f"   Language: {code_output.content['language']}")
    print(f"   Functions: {code_output.content['functions']}")
    print(f"   Complexity: {code_output.content['complexity_score']:.2f}")
    
    # Demo 3: Cross-modal reasoning
    print("\n[3] Cross-Modal Reasoning:")
    cross_modal_result = mmai.cross_modal_reasoning([text_input, code_input])
    print(f"   Modalities: {', '.join(cross_modal_result['input_modalities'])}")
    print(f"   Insights: {len(cross_modal_result['cross_modal_insights'])}")
    
    print("\n" + "=" * 70)
    print("⚡ Multi-Modal AI Ready ⚡")
    print("=" * 70)

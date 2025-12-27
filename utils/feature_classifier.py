#!/usr/bin/env python3
"""
Feature Type Classifier

Automatically detect feature type to determine workflow steps:
- UI_CHANGE: New UI components, requires screenshots
- DATA_ENHANCEMENT: Backend/API only, skip screenshots
- INFRASTRUCTURE: Config/tooling, skip screenshots & announcements
- DOCUMENTATION_ONLY: Docs changes, minimal workflow
"""

from typing import List, Dict, Tuple
from enum import Enum
import re


class FeatureType(Enum):
    """Feature classification types"""
    UI_CHANGE = "ui_change"
    DATA_ENHANCEMENT = "data_enhancement"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION_ONLY = "documentation_only"
    MIXED = "mixed"


class FeatureClassifier:
    """Classify features based on code changes"""

    # File patterns that indicate UI changes
    UI_PATTERNS = [
        r'\.tsx$',
        r'\.jsx$',
        r'/components/',
        r'/pages/',
        r'/app/',
        r'\.css$',
        r'\.scss$',
        r'/styles/'
    ]

    # File patterns that indicate backend/data changes
    BACKEND_PATTERNS = [
        r'/service\.ts$',
        r'/api/',
        r'\.graphql$',
        r'/migrations/',
        r'/schema/',
        r'/models/',
        r'/server/'
    ]

    # File patterns that indicate infrastructure
    INFRA_PATTERNS = [
        r'\.yaml$',
        r'\.yml$',
        r'\.json$',
        r'package\.json',
        r'tsconfig',
        r'\.config\.',
        r'/scripts/',
        r'Dockerfile',
        r'\.env'
    ]

    # File patterns for documentation
    DOC_PATTERNS = [
        r'\.md$',
        r'/docs/',
        r'README',
        r'/documentation/'
    ]

    def __init__(self):
        self.ui_score = 0
        self.backend_score = 0
        self.infra_score = 0
        self.doc_score = 0

    def classify_file(self, filepath: str) -> Tuple[str, int]:
        """
        Classify a single file and return category with confidence score

        Returns:
            Tuple of (category, score) where category is one of:
            'ui', 'backend', 'infra', 'doc', or 'unknown'
        """
        # UI detection
        for pattern in self.UI_PATTERNS:
            if re.search(pattern, filepath):
                return ('ui', 10)

        # Backend detection
        for pattern in self.BACKEND_PATTERNS:
            if re.search(pattern, filepath):
                return ('backend', 8)

        # Infrastructure detection
        for pattern in self.INFRA_PATTERNS:
            if re.search(pattern, filepath):
                return ('infra', 5)

        # Documentation detection
        for pattern in self.DOC_PATTERNS:
            if re.search(pattern, filepath):
                return ('doc', 3)

        return ('unknown', 1)

    def classify(self, changed_files: List[str], commits: List[Dict] = None) -> Dict:
        """
        Classify a feature based on changed files and optionally commit messages

        Args:
            changed_files: List of file paths that changed
            commits: Optional list of commit dicts with 'message' key

        Returns:
            Dict with:
            - type: FeatureType enum
            - confidence: 0-100 score
            - reasoning: List of reasons for classification
            - workflow: Dict of steps to include/skip
        """
        if not changed_files:
            return {
                'type': FeatureType.INFRASTRUCTURE,
                'confidence': 0,
                'reasoning': ['No files provided'],
                'workflow': self._get_workflow(FeatureType.INFRASTRUCTURE)
            }

        # Score each file
        scores = {
            'ui': 0,
            'backend': 0,
            'infra': 0,
            'doc': 0
        }

        file_breakdown = []

        for filepath in changed_files:
            category, score = self.classify_file(filepath)
            if category != 'unknown':
                scores[category] += score
                file_breakdown.append({
                    'file': filepath,
                    'category': category,
                    'score': score
                })

        # Analyze commit messages for additional context
        commit_hints = self._analyze_commits(commits) if commits else {}

        # Determine feature type based on scores
        feature_type = self._determine_type(scores, commit_hints)
        confidence = self._calculate_confidence(scores, feature_type)
        reasoning = self._build_reasoning(scores, file_breakdown, commit_hints, feature_type)

        return {
            'type': feature_type,
            'confidence': confidence,
            'reasoning': reasoning,
            'file_breakdown': file_breakdown,
            'scores': scores,
            'workflow': self._get_workflow(feature_type)
        }

    def _analyze_commits(self, commits: List[Dict]) -> Dict:
        """Extract hints from commit messages"""
        hints = {
            'has_ui_keywords': False,
            'has_data_keywords': False,
            'has_infra_keywords': False
        }

        ui_keywords = ['component', 'ui', 'view', 'page', 'modal', 'form', 'button']
        data_keywords = ['export', 'csv', 'api', 'endpoint', 'query', 'column', 'field']
        infra_keywords = ['config', 'setup', 'migration', 'schema', 'deps']

        for commit in commits:
            message = commit.get('message', '').lower()

            if any(kw in message for kw in ui_keywords):
                hints['has_ui_keywords'] = True
            if any(kw in message for kw in data_keywords):
                hints['has_data_keywords'] = True
            if any(kw in message for kw in infra_keywords):
                hints['has_infra_keywords'] = True

        return hints

    def _determine_type(self, scores: Dict, commit_hints: Dict) -> FeatureType:
        """Determine feature type from scores and hints"""
        total_score = sum(scores.values())

        if total_score == 0:
            return FeatureType.INFRASTRUCTURE

        # Calculate percentages
        ui_pct = (scores['ui'] / total_score) * 100 if total_score > 0 else 0
        backend_pct = (scores['backend'] / total_score) * 100 if total_score > 0 else 0
        doc_pct = (scores['doc'] / total_score) * 100 if total_score > 0 else 0

        # Pure documentation
        if doc_pct > 80:
            return FeatureType.DOCUMENTATION_ONLY

        # UI changes (requires screenshots)
        if ui_pct > 30:
            return FeatureType.UI_CHANGE

        # Backend/data enhancement (no UI)
        if backend_pct > 50 and ui_pct < 10:
            # Double-check with commit messages
            if commit_hints.get('has_data_keywords') and not commit_hints.get('has_ui_keywords'):
                return FeatureType.DATA_ENHANCEMENT
            return FeatureType.DATA_ENHANCEMENT

        # Mixed changes
        if ui_pct > 10 and backend_pct > 10:
            return FeatureType.MIXED

        # Default to infrastructure
        return FeatureType.INFRASTRUCTURE

    def _calculate_confidence(self, scores: Dict, feature_type: FeatureType) -> int:
        """Calculate confidence score (0-100)"""
        total = sum(scores.values())

        if total == 0:
            return 50  # Medium confidence for no files

        # For UI_CHANGE, confidence based on UI score dominance
        if feature_type == FeatureType.UI_CHANGE:
            return min(100, int((scores['ui'] / total) * 150))

        # For DATA_ENHANCEMENT, confidence based on backend score
        if feature_type == FeatureType.DATA_ENHANCEMENT:
            backend_ratio = scores['backend'] / total
            ui_ratio = scores['ui'] / total
            # High confidence if backend dominant and no UI
            if backend_ratio > 0.7 and ui_ratio < 0.1:
                return 95
            elif backend_ratio > 0.5:
                return 80
            return 60

        # For DOCUMENTATION_ONLY
        if feature_type == FeatureType.DOCUMENTATION_ONLY:
            return min(100, int((scores['doc'] / total) * 120))

        # For MIXED or INFRASTRUCTURE
        return 70

    def _build_reasoning(self, scores: Dict, file_breakdown: List[Dict],
                        commit_hints: Dict, feature_type: FeatureType) -> List[str]:
        """Build human-readable reasoning"""
        reasons = []

        total = sum(scores.values())

        # File-based reasoning
        if scores['ui'] > 0:
            ui_files = [f['file'] for f in file_breakdown if f['category'] == 'ui']
            reasons.append(f"Found {len(ui_files)} UI file(s): {', '.join(ui_files[:3])}")

        if scores['backend'] > 0:
            backend_files = [f['file'] for f in file_breakdown if f['category'] == 'backend']
            reasons.append(f"Found {len(backend_files)} backend file(s): {', '.join(backend_files[:3])}")

        if scores['doc'] > 0:
            doc_files = [f['file'] for f in file_breakdown if f['category'] == 'doc']
            reasons.append(f"Found {len(doc_files)} documentation file(s)")

        # Type-specific reasoning
        if feature_type == FeatureType.UI_CHANGE:
            reasons.append("✅ UI changes detected - screenshots required")
        elif feature_type == FeatureType.DATA_ENHANCEMENT:
            reasons.append("✅ Data/backend changes only - no UI modifications")
            reasons.append("⏭️  Screenshots not needed")
        elif feature_type == FeatureType.DOCUMENTATION_ONLY:
            reasons.append("📄 Documentation-only changes")
            reasons.append("⏭️  Skip screenshots and full workflow")
        elif feature_type == FeatureType.INFRASTRUCTURE:
            reasons.append("🔧 Infrastructure/config changes")
            reasons.append("⏭️  Minimal announcement workflow")

        # Commit message hints
        if commit_hints.get('has_data_keywords'):
            reasons.append("Commit messages mention data/export changes")
        if commit_hints.get('has_ui_keywords'):
            reasons.append("Commit messages mention UI components")

        return reasons

    def _get_workflow(self, feature_type: FeatureType) -> Dict:
        """Define which workflow steps to include for each feature type"""
        workflows = {
            FeatureType.UI_CHANGE: {
                'research': True,
                'capture_screenshots': True,
                'upload_screenshots': True,
                'create_documentation': True,
                'sync_documentation': True,
                'create_announcements': True,
                'summary': True
            },
            FeatureType.DATA_ENHANCEMENT: {
                'research': True,
                'capture_screenshots': False,  # Skip
                'upload_screenshots': False,   # Skip
                'create_documentation': True,
                'sync_documentation': True,
                'create_announcements': True,
                'summary': True
            },
            FeatureType.INFRASTRUCTURE: {
                'research': True,
                'capture_screenshots': False,
                'upload_screenshots': False,
                'create_documentation': True,
                'sync_documentation': False,  # Optional
                'create_announcements': False,  # Usually not needed
                'summary': True
            },
            FeatureType.DOCUMENTATION_ONLY: {
                'research': True,
                'capture_screenshots': False,
                'upload_screenshots': False,
                'create_documentation': False,  # Already done
                'sync_documentation': True,
                'create_announcements': False,
                'summary': True
            },
            FeatureType.MIXED: {
                'research': True,
                'capture_screenshots': True,
                'upload_screenshots': True,
                'create_documentation': True,
                'sync_documentation': True,
                'create_announcements': True,
                'summary': True
            }
        }

        return workflows.get(feature_type, workflows[FeatureType.MIXED])


def classify_feature(changed_files: List[str], commits: List[Dict] = None) -> Dict:
    """
    Convenience function to classify a feature

    Usage:
        result = classify_feature(['apps/admin-app/src/service.ts', 'migrations/add_column.sql'])
        print(f"Type: {result['type']}")
        print(f"Skip screenshots: {not result['workflow']['capture_screenshots']}")
    """
    classifier = FeatureClassifier()
    return classifier.classify(changed_files, commits)


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python feature_classifier.py <file1> <file2> ...")
        sys.exit(1)

    files = sys.argv[1:]
    result = classify_feature(files)

    print(f"\n🔍 Feature Classification Results")
    print(f"=" * 60)
    print(f"Type: {result['type'].value}")
    print(f"Confidence: {result['confidence']}%")
    print(f"\nReasoning:")
    for reason in result['reasoning']:
        print(f"  - {reason}")
    print(f"\nWorkflow Steps:")
    for step, include in result['workflow'].items():
        status = "✅" if include else "⏭️ "
        print(f"  {status} {step}")
    print(f"\nScores: {result['scores']}")

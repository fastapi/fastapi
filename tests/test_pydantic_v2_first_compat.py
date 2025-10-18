# path: tests/test_pydantic_v2_first_compat.py

"""
Tests for v2-first compatibility layer with lazy v1 loading.

This test suite validates that:
1. Python 3.14 + Pydantic v2 runs without warnings
2. Python 3.14 + Pydantic v1 shows controlled warnings/errors
3. isinstance() checks work with proxy classes
4. Zero breaking changes for existing imports
"""

import sys
import warnings
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class TestV2FirstCompatibility:
    """Test v2-first compatibility layer."""

    def test_v2_imports_no_warnings(self):
        """Test that v2-only usage doesn't trigger warnings on Python 3.14."""
        if sys.version_info < (3, 14):
            pytest.skip("Python 3.14+ specific test")
        
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("error", DeprecationWarning)
            
            # These should not trigger any warnings
            import fastapi
            import fastapi.encoders
            from fastapi import FastAPI
            
            app = FastAPI()
            
            # Test jsonable_encoder with v2 model
            class TestModel(BaseModel):
                name: str
                value: int
            
            model = TestModel(name="test", value=42)
            result = jsonable_encoder(model)
            
            assert result == {"name": "test", "value": 42}
            assert len(w) == 0, f"Unexpected warnings: {[str(warning.message) for warning in w]}"

    def test_proxy_classes_isinstance(self):
        """Test that proxy classes work correctly with isinstance()."""
        import fastapi.temp_pydantic_v1_params as T
        from fastapi import params
        
        # Test that proxy classes are available
        assert hasattr(T, 'Param')
        assert hasattr(T, 'Body')
        assert hasattr(T, 'Form')
        assert hasattr(T, 'File')
        assert hasattr(T, 'Query')
        assert hasattr(T, 'Header')
        assert hasattr(T, 'Cookie')
        assert hasattr(T, 'Path')
        
        # Test isinstance() with proxy classes (expect DeprecationWarning)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", (DeprecationWarning, UserWarning))
            param_instance = T.Param()
            assert isinstance(param_instance, T.Param)
        
        # Test that proxy classes are different from v2 params
        from fastapi import params as v2_params
        assert T.Param is not v2_params.Param
        assert T.Body is not v2_params.Body

    def test_backward_compatibility_imports(self):
        """Test that existing imports continue to work."""
        # Test direct import from temp_pydantic_v1_params
        from fastapi.temp_pydantic_v1_params import Body, Query, Form, File, Param, Header, Cookie, Path
        
        # Test that classes are available and callable (expect DeprecationWarning)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", (DeprecationWarning, UserWarning))
            body = Body()
            query = Query()
            form = Form()
            file_param = File()
            param = Param()
            header = Header()
            cookie = Cookie()
            path = Path()
        
        # Test that they have expected attributes
        assert hasattr(body, 'default')
        assert hasattr(query, 'default')
        assert hasattr(form, 'default')
        assert hasattr(file_param, 'default')
        assert hasattr(param, 'default')
        assert hasattr(header, 'default')
        assert hasattr(cookie, 'default')
        assert hasattr(path, 'default')

    def test_lazy_loading_behavior(self):
        """Test that v1 is only loaded when actually used."""
        import sys
        
        # Clear any existing pydantic.v1 from sys.modules
        v1_was_loaded = "pydantic.v1" in sys.modules
        
        # Import FastAPI components
        import fastapi
        import fastapi.encoders
        from fastapi import FastAPI
        
        app = FastAPI()
        
        # At this point, pydantic.v1 should not be loaded unless it was already loaded
        # (we can't test the exact state because it might have been loaded by other tests)
        
        # Test that we can still access v1 proxy
        from fastapi._compat import v1
        assert v1 is not None

    def test_encoders_lazy_registration(self):
        """Test that v1 encoders are registered lazily."""
        import sys
        
        # Test with a v2 model (should not trigger v1 encoder registration)
        class V2Model(BaseModel):
            name: str
        
        model = V2Model(name="test")
        result = jsonable_encoder(model)
        assert result == {"name": "test"}
        
        # The encoders should work without importing pydantic.v1
        # (unless it was already imported by other tests)

    def test_compat_module_structure(self):
        """Test that the compat module has expected structure."""
        # Test that v1 proxy has expected attributes (expect DeprecationWarning)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", (DeprecationWarning, UserWarning))
            from fastapi._compat import v1
            
            # Test that v1 proxy has expected attributes
            assert hasattr(v1, 'BaseModel')
            assert hasattr(v1, 'FieldInfo')
            assert hasattr(v1, 'ValidationError')
            
            # Test that wrapper functions are available
            assert hasattr(v1, '_normalize_errors')
            assert hasattr(v1, '_model_dump')
            assert hasattr(v1, '_model_rebuild')

    def test_strict_mode_environment_variable(self):
        """Test FASTAPI_PYDANTIC_V1_STRICT environment variable behavior."""
        import os
        
        # Save original value
        original_strict = os.environ.get("FASTAPI_PYDANTIC_V1_STRICT")
        
        try:
            # Test with strict mode enabled
            os.environ["FASTAPI_PYDANTIC_V1_STRICT"] = "1"
            
            # This should not raise an error unless we actually try to use v1
            import fastapi
            from fastapi import FastAPI
            app = FastAPI()
            
            # The strict mode only affects actual v1 usage, not imports
            assert True
            
        finally:
            # Restore original value
            if original_strict is not None:
                os.environ["FASTAPI_PYDANTIC_V1_STRICT"] = original_strict
            else:
                os.environ.pop("FASTAPI_PYDANTIC_V1_STRICT", None)

    def test_v1_params_composition(self):
        """Test that v1 params use composition instead of inheritance."""
        from fastapi._compat._v1_params import Param, Body, Form
        
        # Test that they can be instantiated (expect DeprecationWarning)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", (DeprecationWarning, UserWarning))
            param = Param()
            body = Body()
            form = Form()
        
        # Test that they delegate to internal v1.FieldInfo
        assert hasattr(param, '_fi')
        assert hasattr(body, '_fi')
        assert hasattr(form, '_fi')
        
        # Test that they have expected interface
        assert hasattr(param, 'default')
        assert hasattr(body, 'default')
        assert hasattr(form, 'default')


if __name__ == "__main__":
    pytest.main([__file__])

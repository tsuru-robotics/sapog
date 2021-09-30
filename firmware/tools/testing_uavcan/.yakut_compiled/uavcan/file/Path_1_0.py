# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/file/Path.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.922020 UTC
# Is deprecated: yes
# Fixed port ID: None
# Full name:     uavcan.file.Path
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import warnings as _warnings_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Path_1_0(_dsdl_.CompositeObject):
    """
    Generated property settings use relaxed type signatures, accepting a large variety of
    possible representations of the value, which are automatically converted to a well-defined
    internal representation. When accessing a property, this strict well-defined internal
    representation is always returned. The implicit strictification enables more precise static
    type analysis.

    The value returned by the __repr__() method may be invariant to some of the field values,
    and its format is not guaranteed to be stable. Therefore, the returned string representation
    can be used only for displaying purposes; any kind of automation build on top of that will
    be fragile and prone to mismaintenance.
    """
    SEPARATOR:  int = 47
    MAX_LENGTH: int = 112

    def __init__(self,
                 path: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None) -> None:
        """
        uavcan.file.Path.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param path: saturated uint8[<=112] path
        """
        _warnings_.warn('Data type uavcan.file.Path.1.0 is deprecated', DeprecationWarning)

        self._path: _np_.ndarray

        if path is None:
            self.path = _np_.array([], _np_.uint8)
        else:
            path = path.encode() if isinstance(path, str) else path  # Implicit string encoding
            if isinstance(path, (bytes, bytearray)) and len(path) <= 112:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._path = _np_.frombuffer(path, _np_.uint8)
            elif isinstance(path, _np_.ndarray) and path.dtype == _np_.uint8 and path.ndim == 1 and path.size <= 112:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._path = path
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                path = _np_.array(path, _np_.uint8).flatten()
                if not path.size <= 112:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'path: invalid array length: not {path.size} <= 112')
                self._path = path
            assert isinstance(self._path, _np_.ndarray)
            assert self._path.dtype == _np_.uint8
            assert self._path.ndim == 1
            assert len(self._path) <= 112

    @property
    def path(self) -> _np_.ndarray:
        """
        saturated uint8[<=112] path
        DSDL does not support strings natively yet. To interpret this array as a string,
        use tobytes() to convert the NumPy array to bytes, and then decode() to convert bytes to string:
        .path.tobytes().decode()
        When assigning a string to this property, no manual conversion is necessary (it will happen automatically).
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._path

    @path.setter
    def path(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]) -> None:
        x = x.encode() if isinstance(x, str) else x  # Implicit string encoding
        if isinstance(x, (bytes, bytearray)) and len(x) <= 112:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._path = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 112:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._path = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size <= 112:  # Length cannot be checked before casting and flattening
                raise ValueError(f'path: invalid array length: not {x.size} <= 112')
            self._path = x
        assert isinstance(self._path, _np_.ndarray)
        assert self._path.dtype == _np_.uint8
        assert self._path.ndim == 1
        assert len(self._path) <= 112

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Path_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.path) <= 112, 'self.path: saturated uint8[<=112]'
        _ser_.add_aligned_u8(len(self.path))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.path)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 904, \
            'Bad serialization of uavcan.file.Path.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Path_1_0._DeserializerTypeVar_) -> Path_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "path"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 112:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 112')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len0_)
        assert len(_f0_) <= 112, 'saturated uint8[<=112]'
        self = Path_1_0(
            path=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 904, \
            'Bad deserialization of uavcan.file.Path.1.0'
        assert isinstance(self, Path_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'path=%s' % repr(bytes(self.path))[1:],
        ])
        return f'uavcan.file.Path.1.0({_o_0_})'

    _EXTENT_BYTES_ = 113

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{?|pZI2X15MI0kmPJ5BCGjP+7d3kc%nH5{Ke?Wqn&po3I0#~}(=$`M-7?cX>F&9`B{6{y8cZgUg!b<mt7c|z?|_T@'
        'WoD|oo~nAP`ssbV{LjDLPW`Jc6|>Z(S;QS!B{KC$#2G|9F?nH}@(`*sx4kVBUs~9i6%d|>)hFTi(65ejEpl9cqZGS|(9u|-<CgF;'
        'R9(Ic)+wWd>{KW3w(rlw=-8<9XLu5-(_DCORa|;-;Q@jjk;eY6P#s@akfn?8J)R0LxTl<|_l|J4R?I?m@vcBCT5f`#csV5N;abjc'
        '$RG#pTf8IEDXhwsSG&05!X53@L__+c_Ami^81FQXmFHO<E{wXEY$BZJxk(|&cdK`{=0M~Yt>M}REg?glKf-pX-r~*+oeG;C1bSM='
        ')hR?OM56pGjEd^bc8QOPoF;ksev^c}H0nwwS4PJOQhrR{%RJ6ps6LsOw*bdV{fpnBdi`7F8`5s$XIoyi#7z+@b`*%4<*~_Bf+TG~'
        'Zjd~W?Y~uk72endNhf$B6}D7<R=vGubRs<HS8k=EX{QBE!-D(IZI)Rk?ChnTC-|<&N(g_4{;2!R#qx`mjO*xiaa-sKY(oKF9hK5U'
        'o{K%C79GB+jdE>{Rr8lCjZLB#+_v#}sX9qrEi*y>qhqwU^K8^@o+UOO_6niv`QI#Kz>IETTedcyF3F!><st9jHi{*WSIb3xnwEKL'
        'kjzd%<Jqc<RMBwkx1%pFywLKG>SiOrsoOWUhTFrPTiE~m@)x;QeK2ntre(oVUWdlIyIprcWOH=%IW@K-AuCQ!cfEbb_3E|HzX~*4'
        'b-EA!FPYxP@E*T;WApo+AKGjrv?1hg)za0g*Y?4nx^O@scsy&QhCqLo=VdH^l~(E!k68*>22D;Ho>ph^80<mH3u8T3Y1pjJb7xAM'
        '04H(c4V`)*O%4O6G8C!7qcRqI11AbI8H|<9r^3R(8<V*KhW1KNc%yHFqKt8<xrGUK8v`!%#|_#o6lFjX7+sA%jT$4K0xpHa;Fk0S'
        '1!Y$y5dM<)?|rz`>1<*UNEyLIy&)q6=4NQi8KuiWC#Vc5Q<~k`S-&2!9SO|nY{qcVRmvP7Fby$Nj(J=g8;dpILMEJKD}xn+byx=h'
        '*S0<ySDA$|>N4}D_Oix!mMY{Dp=PX4w#+2;FfcP_Q>hY3AyODCR6Q2YYCkFm>}u581|$VXsKLdo!LdF>lZdTE5r)I+nWh-6KdM{('
        'jYkk?k0|Ji%u7>FBm!fgT+CP^>A+I$b!8=8LKq8Az%Fu06Uq7n0vfAMAYJ{s$JiA%Y^W=Y($qkzQ8dgVO@d`gKO|ejHHOTZQ~*<&'
        'Ds&VJR->Z<7i=MFZJ7fvR$BB|BloD4C?hH_+h#W^ia1CKk)256Kr`Xc(OZ$i6*C^Q82l8_Om{SL9;*y*g9bkZC=Q07-`tM)?h%Po'
        'W1YW(w-FGccG#>oY%^N>vGF`&lkp5(ZksQ%%uF3U_B}B}qrFg?ND=cXQ?))N(8IZ@%W8Vf493S`!eUG5>|lANe(0K3U`$Q3I5li-'
        'xXISPW2ibgxG2cWa?t3+wL@xtZcC&oMtn)darI053sN-8c>R`#MR#9fqyGTs|AJ}>2><{'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

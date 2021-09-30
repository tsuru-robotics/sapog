# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/metatransport/ethernet/Frame.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:51.770867 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.metatransport.ethernet.Frame
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.metatransport.ethernet


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Frame_0_1(_dsdl_.CompositeObject):
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
    def __init__(self,
                 destination: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]] = None,
                 source:      _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]] = None,
                 ethertype:   _ty_.Optional[uavcan.metatransport.ethernet.EtherType_0_1] = None,
                 payload:     _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None) -> None:
        """
        uavcan.metatransport.ethernet.Frame.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param destination: saturated uint8[6] destination
        :param source:      saturated uint8[6] source
        :param ethertype:   uavcan.metatransport.ethernet.EtherType.0.1 ethertype
        :param payload:     saturated uint8[<=9216] payload
        """
        self._destination: _np_.ndarray
        self._source:      _np_.ndarray
        self._ethertype:   uavcan.metatransport.ethernet.EtherType_0_1
        self._payload:     _np_.ndarray

        if destination is None:
            self.destination = _np_.zeros(6, _np_.uint8)
        else:
            if isinstance(destination, (bytes, bytearray)) and len(destination) == 6:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._destination = _np_.frombuffer(destination, _np_.uint8)
            elif isinstance(destination, _np_.ndarray) and destination.dtype == _np_.uint8 and destination.ndim == 1 and destination.size == 6:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._destination = destination
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                destination = _np_.array(destination, _np_.uint8).flatten()
                if not destination.size == 6:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'destination: invalid array length: not {destination.size} == 6')
                self._destination = destination
            assert isinstance(self._destination, _np_.ndarray)
            assert self._destination.dtype == _np_.uint8
            assert self._destination.ndim == 1
            assert len(self._destination) == 6

        if source is None:
            self.source = _np_.zeros(6, _np_.uint8)
        else:
            if isinstance(source, (bytes, bytearray)) and len(source) == 6:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._source = _np_.frombuffer(source, _np_.uint8)
            elif isinstance(source, _np_.ndarray) and source.dtype == _np_.uint8 and source.ndim == 1 and source.size == 6:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._source = source
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                source = _np_.array(source, _np_.uint8).flatten()
                if not source.size == 6:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'source: invalid array length: not {source.size} == 6')
                self._source = source
            assert isinstance(self._source, _np_.ndarray)
            assert self._source.dtype == _np_.uint8
            assert self._source.ndim == 1
            assert len(self._source) == 6

        if ethertype is None:
            self.ethertype = uavcan.metatransport.ethernet.EtherType_0_1()
        elif isinstance(ethertype, uavcan.metatransport.ethernet.EtherType_0_1):
            self.ethertype = ethertype
        else:
            raise ValueError(f'ethertype: expected uavcan.metatransport.ethernet.EtherType_0_1 '
                             f'got {type(ethertype).__name__}')

        if payload is None:
            self.payload = _np_.array([], _np_.uint8)
        else:
            payload = payload.encode() if isinstance(payload, str) else payload  # Implicit string encoding
            if isinstance(payload, (bytes, bytearray)) and len(payload) <= 9216:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._payload = _np_.frombuffer(payload, _np_.uint8)
            elif isinstance(payload, _np_.ndarray) and payload.dtype == _np_.uint8 and payload.ndim == 1 and payload.size <= 9216:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._payload = payload
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                payload = _np_.array(payload, _np_.uint8).flatten()
                if not payload.size <= 9216:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'payload: invalid array length: not {payload.size} <= 9216')
                self._payload = payload
            assert isinstance(self._payload, _np_.ndarray)
            assert self._payload.dtype == _np_.uint8
            assert self._payload.ndim == 1
            assert len(self._payload) <= 9216

    @property
    def destination(self) -> _np_.ndarray:
        """
        saturated uint8[6] destination
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._destination

    @destination.setter
    def destination(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]) -> None:
        if isinstance(x, (bytes, bytearray)) and len(x) == 6:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._destination = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size == 6:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._destination = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size == 6:  # Length cannot be checked before casting and flattening
                raise ValueError(f'destination: invalid array length: not {x.size} == 6')
            self._destination = x
        assert isinstance(self._destination, _np_.ndarray)
        assert self._destination.dtype == _np_.uint8
        assert self._destination.ndim == 1
        assert len(self._destination) == 6

    @property
    def source(self) -> _np_.ndarray:
        """
        saturated uint8[6] source
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._source

    @source.setter
    def source(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]) -> None:
        if isinstance(x, (bytes, bytearray)) and len(x) == 6:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._source = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size == 6:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._source = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size == 6:  # Length cannot be checked before casting and flattening
                raise ValueError(f'source: invalid array length: not {x.size} == 6')
            self._source = x
        assert isinstance(self._source, _np_.ndarray)
        assert self._source.dtype == _np_.uint8
        assert self._source.ndim == 1
        assert len(self._source) == 6

    @property
    def ethertype(self) -> uavcan.metatransport.ethernet.EtherType_0_1:
        """
        uavcan.metatransport.ethernet.EtherType.0.1 ethertype
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._ethertype

    @ethertype.setter
    def ethertype(self, x: uavcan.metatransport.ethernet.EtherType_0_1) -> None:
        if isinstance(x, uavcan.metatransport.ethernet.EtherType_0_1):
            self._ethertype = x
        else:
            raise ValueError(f'ethertype: expected uavcan.metatransport.ethernet.EtherType_0_1 got {type(x).__name__}')

    @property
    def payload(self) -> _np_.ndarray:
        """
        saturated uint8[<=9216] payload
        DSDL does not support strings natively yet. To interpret this array as a string,
        use tobytes() to convert the NumPy array to bytes, and then decode() to convert bytes to string:
        .payload.tobytes().decode()
        When assigning a string to this property, no manual conversion is necessary (it will happen automatically).
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._payload

    @payload.setter
    def payload(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]) -> None:
        x = x.encode() if isinstance(x, str) else x  # Implicit string encoding
        if isinstance(x, (bytes, bytearray)) and len(x) <= 9216:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._payload = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 9216:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._payload = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size <= 9216:  # Length cannot be checked before casting and flattening
                raise ValueError(f'payload: invalid array length: not {x.size} <= 9216')
            self._payload = x
        assert isinstance(self._payload, _np_.ndarray)
        assert self._payload.dtype == _np_.uint8
        assert self._payload.ndim == 1
        assert len(self._payload) <= 9216

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Frame_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        assert len(self.destination) == 6, 'self.destination: saturated uint8[6]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.destination)
        assert len(self.source) == 6, 'self.source: saturated uint8[6]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.source)
        _ser_.pad_to_alignment(8)
        self.ethertype._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.payload) <= 9216, 'self.payload: saturated uint8[<=9216]'
        _ser_.add_aligned_u16(len(self.payload))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.payload)
        _ser_.pad_to_alignment(8)
        assert 128 <= (_ser_.current_bit_length - _base_offset_) <= 73856, \
            'Bad serialization of uavcan.metatransport.ethernet.Frame.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Frame_0_1._DeserializerTypeVar_) -> Frame_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "destination"
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, 6)
        assert len(_f0_) == 6, 'saturated uint8[6]'
        # Temporary _f1_ holds the value of "source"
        _f1_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, 6)
        assert len(_f1_) == 6, 'saturated uint8[6]'
        # Temporary _f2_ holds the value of "ethertype"
        _des_.pad_to_alignment(8)
        _f2_ = uavcan.metatransport.ethernet.EtherType_0_1._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f3_ holds the value of "payload"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u16()
        assert _len0_ >= 0
        if _len0_ > 9216:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 9216')
        _f3_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len0_)
        assert len(_f3_) <= 9216, 'saturated uint8[<=9216]'
        self = Frame_0_1(
            destination=_f0_,
            source=_f1_,
            ethertype=_f2_,
            payload=_f3_)
        _des_.pad_to_alignment(8)
        assert 128 <= (_des_.consumed_bit_length - _base_offset_) <= 73856, \
            'Bad deserialization of uavcan.metatransport.ethernet.Frame.0.1'
        assert isinstance(self, Frame_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'destination=%s' % _np_.array2string(self.destination, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
            'source=%s' % _np_.array2string(self.source, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
            'ethertype=%s' % self.ethertype,
            'payload=%s' % _np_.array2string(self.payload, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.metatransport.ethernet.Frame.0.1({_o_0_})'

    _EXTENT_BYTES_ = 9232

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{^{MTW=dh6n5HNoTe@5g;w0u5tLpKSvxmWkSgjHr*$_mAxR@4K+~~zlC#a;G&5`JB1DT+M5K{g==K4Lr%Ld~BN7sS'
        'f}g~h-F0jyaS#s>De`#c%s1!EeBXEcaQOL?i9-6P&qZxVI-W%(7cTSM2dv?7i#9_)3Z<)fqK~aA5jRyV_*y&S$+P70qvY%4k{+P}'
        '^Kt#Hn6;WLuzaqV5-gBWD3rw&a1n52Er>L#NLyS;Hw+Re=&|*D{4B8x_Rx39qeM?orj&3SvEnlM0`UiAwiA`;kp-7~PB)_?)M1KI'
        'Wzy8I4cIOOYbW~jf_tAki#*s=P%%^ewH>3}<30~m4mKc{NVvYM+!jWhx)VruGvH1wP<)e%e!L0Va255^;}W}wnKqeJ)DIn=z^nSq'
        'atFw4vu@zpl36m>^Eg?-bg5J<aF}p<fxeF$dK{4=)^t@nu}AeVZFn-#7dq*7gE4cp`+K5~UUyY?39I-uPgftNVU%bx2t>C1M(DXs'
        'EP9FiAzp^UxBNKbf~in+iyoy-aPfV>(kEAV#Fe{$+#$M!xx*~Ry;P4qkBRo~AjE1hFXqXU<dR){DjQh&F!kLavCC$_?wi4wxzN~S'
        '2Gt%ip@pY*G5d`1&iVZa>1lXZj~fO9M)ZWkrE-I`gao0S5bG)=xHg%k2dCgnK6(XS&qwF%A`mzaZ{rid1x)@Typt}$6qNIrS(wj9'
        'SJLV}$O5i*OMnmUGF-#|%6<t$wVUOr3}ewmuH1xMeW@MFM<e>;!7{9xK}t#(gYk~);3z7s2d-P+WVgN%J(691e)@4;yb%V5kUNw)'
        'Xm4$quFs`=;i`V4Ln?d=!KHbOJ{c8P(wAUf2O0N_ZwS^jv&ih?LO#ZIJv>vMyOJ1zq}O!spHewoSy|2#0g<D_mj-5j?q9&96}`6)'
        '(8%oE{LK6g64$4CJdHNmnPD1400%<Yf^Xm}*oMb38id2~LYho*C)w7=>4xzqYTl5#PEyw=Xhs2C@HmYa%3lX1<wvD9+ltkcxz(u$'
        'elR!FDto0UZlFM^;F~B1gzOrlobu6KxF}_GDfQ8%)S*jhhb~sxnzpi7)H?+x@o-_B5v{Q0A}6=urv7a;w<of*ku-CTNWvs>_=bz-'
        'NE&TYt5&OIg>SkN&oxg;DzSo4poI|xA+<`qVjWonR}v3n2!4ivhigRo%=3suRd7YZjh+(}Fhww}bjo$Oz@t=18k`6;@)pLBjZly~'
        'mGv8yx|QrNSG1pH<~VM!xyPe+$#)XviybY>qS4S(El;ABCykan5|+IZ9#8K!Z6|wFd|IDfXV_S<sSIjK1I=fta9*G6`16Koh*{6t'
        '#ojmVA;ZgT(}40{Mp+vM2KySiX*I^r@$pT6-g6;+P-j<Iu*nZ{{ZYD=`Znf2$Q%oB?RJ3-6%O!6F7uneJ$Z0o{t9CeYkMKXrgT$J'
        'uf~yKy)>+8A*EB}A@^czZ)C&#Y?0(r92p|LPi*)4WeeK^hbN}S1vmkpK@EO^&*3llHHIIy;m0~W)A#;6O{Tx3di4m;jrP7x1$Cu7'
        'W6fsj!`Li+!tpsHX^t~Kd!!Z+JjItrJD%H!aIvJCkrVsTyC@-}9)YGDg@K_ph6G#0<Yy$fSgYG>pDtHvb?sJlrCwbteYChntM%#f'
        '()B@t`gv#6o%<sT`_nM!|B9T37xqwpyG=O(pJep8i?esTvoCTz@0$K83yyF$>J842cTNAE1wTY$KFo>P558x`5Y+k`Zg6KAnhO8`'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

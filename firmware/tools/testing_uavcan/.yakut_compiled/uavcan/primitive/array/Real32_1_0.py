# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/array/Real32.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.706593 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Real32
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Real32_1_0(_dsdl_.CompositeObject):
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
                 value: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[float]]] = None) -> None:
        """
        uavcan.primitive.array.Real32.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated float32[<=64] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.float32)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.float32 and value.ndim == 1 and value.size <= 64:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.float32).flatten()
                if not value.size <= 64:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 64')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.float32
            assert self._value.ndim == 1
            assert len(self._value) <= 64

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated float32[<=64] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[float]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.float32 and x.ndim == 1 and x.size <= 64:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.float32).flatten()
            if not x.size <= 64:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 64')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.float32
        assert self._value.ndim == 1
        assert len(self._value) <= 64

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Real32_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 64, 'self.value: saturated float32[<=64]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Real32.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Real32_1_0._DeserializerTypeVar_) -> Real32_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 64:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 64')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.float32, _len0_)
        assert len(_f0_) <= 64, 'saturated float32[<=64]'
        self = Real32_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Real32.1.0'
        assert isinstance(self, Real32_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Real32.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{`t<TW{M|5*F`FoV#;rlcr|VT$Cn}EL*mfOB1!l1}>(P7HPNW1qDq>Cniyf5_oa#E(*90Tc`km66on$AN=T_;Ya@r'
        '_su_JhoTfmb)3YB?O=DU7ag9N@0;(;Iixt6Mfr~}MsnRxJknlh1P!-f2F!OX*ZI+^xvXH;Tg`SWa6-o8!=HzKR1YJceX-DH{C9r!'
        'XZ{n<$BOA$O|qYlthu`7723YjbV6s26)fMk777oU<&KZ>SU2aGA2=<K+qqc#vN!&ng8;c-_|H5ZGOaN5omv#KfPcrglJwY#$I5+&'
        'xs44e2hD~RT4tE)i_dKVPet+g%$F9;(#$8!n+@#`(%Hdv9X6TEn#>D(d|SwQyj&h1xbL>CaFAultU00Sc7t#*NMhXzLbKUwFm9iX'
        'Pk+{jr?A3DWW&@%Y03SYKjiUAGYBoOVfl?Gi8{p7v}Qdgj2da+N4`}LDV+hO`F?Lq9PyR$^5|G)Y`i=<IbN9<t5ha#R!XI*(Q>IW'
        'UapiUN|QIoCd%bep2mu5@c~lTw(3r}z@ZwS=!G*MrD@L6K$?gD=>^WL#~L4dA)96Xz=G`&&~3xM076P>U+NI6Y}Q;-cDbLxjfGGy'
        '!@pni_|S(=m~G4FblGE$C9~D$v9T3Nu+XfvT&K?CVPwq~ZBLqnPutA5!j`|WA*xxo9Xd4jo%qy8Ew65c%zLV9nvB%bXC9r#Joz7e'
        '5V@}9FKqHu%{j}B82^puK~I93eYcm44+wSUq2<l8hpf#)XDdnH({9dF$_emschdeO<uZt?o4=;x(Sb+@<c2vt*3uIcxmJn?A@$8A'
        'Aojkc?l;|6Vghn+PI){B637Xt*|nICwE-I_peCUAa0fQoK%+In!N+)-q3fZi`oRG>n82aTrl+wEZ|Mg^a43Nz1H3d#b4Q<vfx~bl'
        'fnz<r$Div9N8wlkCpN_)3(XI|5FU=hi3Cn&zB1VlrPxz1jD=x1nZW6%Y9K4w&TNYdPQmE}-stC<w7j`(Je+|y5;(i1Ch{QrxtHRF'
        'H{omoZw=&&ti*TzrTO3-yp_P)&(up^<TLV0G2lGBoq*9hU+=s!7mUz-4Hq&V<5|knxbN;rJa`8#Byh1G^NAfu^K)s(V!*p_F@ej^'
        '-4j9><W0U;b~H9zg3Afy`|G4TAw6SPcRU7MfqVk*z3@5-LH^fvMF(7k_Y%0iv9}kAGymlN-q^Lca1E{}P}o);2t}CUu4;lCP)J}j'
        'i*YQy-%7h44~j6Fz}U8PK}f=l?}<Jr!B_(2&1dC0agX-T%fy~(fpI7&F!@qBBQ#;B_EalOz+?iIjps|gn>TvK+}v{=Fa?zaZoPEw'
        'h=K68UyE+I3AYlsv-LSFQ;bS_7T<qu`rtO)N#O1)<(F89<KAms1H2D+6R7rbokUbRviY{<b<6K;b`f&|E((|vaZ$vago_g9WL%VS'
        'M!_`&XH;BMaYiE%OK1qVB%mSUl8A<cOA;C~F3Ff9R}B{x%&EAjVvfcdRAB|H0<H*H6>&wxs)Q>NR%Kj~(I8hHmlQNqTvE}{a7lw1'
        'Si>0s*94pqaZSV-3D+c?k#SANs)8#DR#jY4v8v&UmP9p1)z(*3a(<1vZh!M%Qw{0qd+;t-L;8L-)O`cY?N>v)QVr=lTn!n|d(Q4c'
        'HDnC#!2fJDWMuyf{9jc=>6$NgcXz)U>Q_TLq4N9H(57l=@T}}tL))!}vgb>lY{&Mip;xGevfrcqYG^O2A<A(Q*?-ay^BOLb2-F4a'
        '2+%=Y#Eyu%gdGWW89Oqr$~djys)FkRPOE5(xT@m1h|?O{60T~bU>WlQE(@3!aaqK?gv%1<Wn7lgmT_H%X;{T+0auBD&;%u%gwrzW'
        '#7dzQ)K%=LsB75KaGin>H<=W)DU?P94%o1cHbqcyS;4%D%PN&XX^+TOVkPTA#j@FG)p?xbQO$~npXjNYwS}xz`xCd<?BhW^WHwma'
        'XK4$p!GDd9n2(%!)-c;GKQx^Ne-IxxgI46%85vw=wyn_S@xO|8tI3Li<IXX^_#*|GF9ue-HCue-_{|?IpB2Ma%MFSYF?76HGiwVM'
        '+fmJR>ZZ?TBR37W(W(uKeV2YOwAgLZ7PHQAp;Q<xWFDN>V_N|!@zcI+!2CI<&iJqPU-9HW=B;|@E*O5gq=3w6d)9EW7G-eD`1VF='
        'a%yU7tTcJuxYi$j$L$Hbl6Bl}4|MI0er7cqB!5%4j;!}$og{S49Q0_g0JZ;okZnofKcn(&*k2z200'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

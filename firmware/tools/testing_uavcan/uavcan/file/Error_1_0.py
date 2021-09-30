# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/file/Error.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.400236 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.file.Error
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Error_1_0(_dsdl_.CompositeObject):
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
    OK:             int = 0
    UNKNOWN_ERROR:  int = 65535
    NOT_FOUND:      int = 2
    IO_ERROR:       int = 5
    ACCESS_DENIED:  int = 13
    IS_DIRECTORY:   int = 21
    INVALID_VALUE:  int = 22
    FILE_TOO_LARGE: int = 27
    OUT_OF_SPACE:   int = 28
    NOT_SUPPORTED:  int = 38

    def __init__(self,
                 value: _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None) -> None:
        """
        uavcan.file.Error.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated uint16 value
        """
        self._value: int

        self.value = value if value is not None else 0

    @property
    def value(self) -> int:
        """
        saturated uint16 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[int, _np_.uint16]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 65535:
            self._value = x
        else:
            raise ValueError(f'value: value {x} is not in [0, 65535]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Error_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.add_aligned_u16(max(min(self.value, 65535), 0))
        _ser_.pad_to_alignment(8)
        assert 16 <= (_ser_.current_bit_length - _base_offset_) <= 16, \
            'Bad serialization of uavcan.file.Error.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Error_1_0._DeserializerTypeVar_) -> Error_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _f0_ = _des_.fetch_aligned_u16()
        self = Error_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 16 <= (_des_.consumed_bit_length - _base_offset_) <= 16, \
            'Bad deserialization of uavcan.file.Error.1.0'
        assert isinstance(self, Error_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
        ])
        return f'uavcan.file.Error.1.0({_o_0_})'

    _EXTENT_BYTES_ = 2

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{@j&U2hvj6irIqq-hfprK$uHbU}dHs9EQOw1^i7j*X1d-Dqu>_5nt-yJO!G`=yy#6ITLJ5U7<#0;$6f;Dz7G9ozY6'
        '>Im5n*6iGwbI+YQbM7x!|Nd=ZZuHZ4ieW6{#3hmmP80r&h6!^?l&3{5xnf2yx0NU(RSMP_7R<ad_nw=d%w1g}8BH<1R?<O4Gq=Za'
        'V_k?`7`;daOh}$*2Ilm_<H`7yY0bCh{xHvtzCox`f`_GI(tL+#m+&}UWpt&%SrVV+Um`J8lqgH;vh9W7DOY@eE7rT2<o%4r%}lXA'
        '6R#I@gM?g>gk^mNrnQRT5tWLhdCUyl(zlOJfb2H6hOtLBgcZ&GZUUok5vgbvQxTsBdQpZ@(Uk#BN@Q@A#Cc@&oWa=@y;#dLyGNap'
        'fOWV%8NJh5g?Hh7xHCq$;<pTZ03YgWWP<hHNxkg25KP+ReXZKXfGV7$$q71a=<7W}BReZG-k6LruIIOmEkcHv?4$qVvfTArp8u^!'
        '>OtTKBU-Qlo0BB4qbm>g_ICGXK)mkx9n$c--oX^K`JEY%7MuR1wB~1_w7g%d)!S`yQ1_bkX|%3v@6G^svx!j6pkC|v!Ba%jUo>6j'
        '-gi*lEG-m^9l>Z^{ZZh9bMnlgPC*qo3aE05oM%cpD#zKF3l^zd49x{LJKM7q*YqCmA2tsN{&(w^&cnLfM>_TeJN8jKTsm2<926Um'
        'on9`G3Ud?{eWu2%<WM5@H)zaqSu2g^VV!h*pB(N7U)QG{^3KCq4%zQ^h~FUXqy5@+w9jTaBrD2x_vpwEI@1-fdj`k!`Z+%%;c#q?'
        '7S@3^xCbA@=kNdy;7jn}8+Za82;qB3fx|H<_!WKz4KGS`p_t)wjwnjPywoeC$B$V|id-ndW8>*HBJ)y2jMz&cRwPD0sj9T74(Si2'
        '+O(dq`7F&o-5G2p)uId&9udL%Wnv-E3{!5VXkkoL$KGAFaMh7_yW8%TJDx?)BtRvm5iC>ISqD5~<|PWI>M?0$Yq8v=fXOmZPToU_'
        'o>PaD7fg(7$hGDdCg?k#ocPw6OCqqk_-*vfuedrKeYe@EMe4UmUKs6M1|o-Pm}AMv{1HoY>;g8sKcazc>D2A7kq9{U68J~IeMIA!'
        'XZ<%8!M`@@l}SRy@M07;{xo-6tAEK5TU{|mFs;Qh#5z-+*$#pOdTa*^wu|5eSpG}auW2^whF%$3?YRE|j;?WWjt2k$'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

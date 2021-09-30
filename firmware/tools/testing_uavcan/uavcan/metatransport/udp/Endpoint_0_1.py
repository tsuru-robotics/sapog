# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/metatransport/udp/Endpoint.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:51.749621 UTC
# Is deprecated: yes
# Fixed port ID: None
# Full name:     uavcan.metatransport.udp.Endpoint
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import warnings as _warnings_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Endpoint_0_1(_dsdl_.CompositeObject):
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
                 ip_address:  _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]] = None,
                 mac_address: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]] = None,
                 port:        _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None) -> None:
        """
        uavcan.metatransport.udp.Endpoint.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param ip_address:  saturated uint8[16] ip_address
        :param mac_address: saturated uint8[6] mac_address
        :param port:        saturated uint16 port
        """
        _warnings_.warn('Data type uavcan.metatransport.udp.Endpoint.0.1 is deprecated', DeprecationWarning)

        self._ip_address:  _np_.ndarray
        self._mac_address: _np_.ndarray
        self._port:        int

        if ip_address is None:
            self.ip_address = _np_.zeros(16, _np_.uint8)
        else:
            if isinstance(ip_address, (bytes, bytearray)) and len(ip_address) == 16:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._ip_address = _np_.frombuffer(ip_address, _np_.uint8)
            elif isinstance(ip_address, _np_.ndarray) and ip_address.dtype == _np_.uint8 and ip_address.ndim == 1 and ip_address.size == 16:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._ip_address = ip_address
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                ip_address = _np_.array(ip_address, _np_.uint8).flatten()
                if not ip_address.size == 16:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'ip_address: invalid array length: not {ip_address.size} == 16')
                self._ip_address = ip_address
            assert isinstance(self._ip_address, _np_.ndarray)
            assert self._ip_address.dtype == _np_.uint8
            assert self._ip_address.ndim == 1
            assert len(self._ip_address) == 16

        if mac_address is None:
            self.mac_address = _np_.zeros(6, _np_.uint8)
        else:
            if isinstance(mac_address, (bytes, bytearray)) and len(mac_address) == 6:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._mac_address = _np_.frombuffer(mac_address, _np_.uint8)
            elif isinstance(mac_address, _np_.ndarray) and mac_address.dtype == _np_.uint8 and mac_address.ndim == 1 and mac_address.size == 6:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._mac_address = mac_address
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                mac_address = _np_.array(mac_address, _np_.uint8).flatten()
                if not mac_address.size == 6:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'mac_address: invalid array length: not {mac_address.size} == 6')
                self._mac_address = mac_address
            assert isinstance(self._mac_address, _np_.ndarray)
            assert self._mac_address.dtype == _np_.uint8
            assert self._mac_address.ndim == 1
            assert len(self._mac_address) == 6

        self.port = port if port is not None else 0

    @property
    def ip_address(self) -> _np_.ndarray:
        """
        saturated uint8[16] ip_address
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]) -> None:
        if isinstance(x, (bytes, bytearray)) and len(x) == 16:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._ip_address = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size == 16:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._ip_address = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size == 16:  # Length cannot be checked before casting and flattening
                raise ValueError(f'ip_address: invalid array length: not {x.size} == 16')
            self._ip_address = x
        assert isinstance(self._ip_address, _np_.ndarray)
        assert self._ip_address.dtype == _np_.uint8
        assert self._ip_address.ndim == 1
        assert len(self._ip_address) == 16

    @property
    def mac_address(self) -> _np_.ndarray:
        """
        saturated uint8[6] mac_address
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._mac_address

    @mac_address.setter
    def mac_address(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]) -> None:
        if isinstance(x, (bytes, bytearray)) and len(x) == 6:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._mac_address = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size == 6:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._mac_address = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size == 6:  # Length cannot be checked before casting and flattening
                raise ValueError(f'mac_address: invalid array length: not {x.size} == 6')
            self._mac_address = x
        assert isinstance(self._mac_address, _np_.ndarray)
        assert self._mac_address.dtype == _np_.uint8
        assert self._mac_address.ndim == 1
        assert len(self._mac_address) == 6

    @property
    def port(self) -> int:
        """
        saturated uint16 port
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._port

    @port.setter
    def port(self, x: _ty_.Union[int, _np_.uint16]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 65535:
            self._port = x
        else:
            raise ValueError(f'port: value {x} is not in [0, 65535]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Endpoint_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        assert len(self.ip_address) == 16, 'self.ip_address: saturated uint8[16]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.ip_address)
        assert len(self.mac_address) == 6, 'self.mac_address: saturated uint8[6]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.mac_address)
        _ser_.add_aligned_u16(max(min(self.port, 65535), 0))
        _ser_.skip_bits(64)
        _ser_.pad_to_alignment(8)
        assert 256 <= (_ser_.current_bit_length - _base_offset_) <= 256, \
            'Bad serialization of uavcan.metatransport.udp.Endpoint.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Endpoint_0_1._DeserializerTypeVar_) -> Endpoint_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "ip_address"
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, 16)
        assert len(_f0_) == 16, 'saturated uint8[16]'
        # Temporary _f1_ holds the value of "mac_address"
        _f1_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, 6)
        assert len(_f1_) == 6, 'saturated uint8[6]'
        # Temporary _f2_ holds the value of "port"
        _f2_ = _des_.fetch_aligned_u16()
        _des_.skip_bits(64)
        self = Endpoint_0_1(
            ip_address=_f0_,
            mac_address=_f1_,
            port=_f2_)
        _des_.pad_to_alignment(8)
        assert 256 <= (_des_.consumed_bit_length - _base_offset_) <= 256, \
            'Bad deserialization of uavcan.metatransport.udp.Endpoint.0.1'
        assert isinstance(self, Endpoint_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'ip_address=%s' % _np_.array2string(self.ip_address, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
            'mac_address=%s' % _np_.array2string(self.mac_address, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
            'port=%s' % self.port,
        ])
        return f'uavcan.metatransport.udp.Endpoint.0.1({_o_0_})'

    _EXTENT_BYTES_ = 32

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{^X+TW=Fb6vv&!b`m=Yxe*}T778KIX1x%gl$Mf|770y5BW`ciYSues2JGF{?yQTEDg_}Bl~(FVY(GTb_y~NBst<jv'
        ')KAc-s^{1z7rRMc+DOiS_RN_xXJ+>|b2f`V{a!6}{<4!%+fV$4?It2tyrG_RuOV!=9yX&eQCj5L_<bFxb)ClIK|2!p+x+~C{QG<{'
        'E4cx0LjS3hx9U8wn?iFP^B{@BSlg)|*<S^I6skby*@)W`aiYQ?mxXNj5w+jutiT3d=P&ZC>T<1P<)vCA`L_^#pS-rc@~m`QiH5(E'
        'PsR1Q=B~yhv!nYAk7M4>v)S9~nee|B!G@NrXzE?rxGNf>DFRKw_Q@rRRa0rz0*{%8L83MS;ok|g*bs4VysGOd?KV2o<!l5pt@A{?'
        '&CnOQoX_Ugw*uiX`xf-AVHa-CtNb3M>n559K9Bv~f!?HEHVTm<URS!Ev&pRJdW|H{7PiveafZxw|8t&=eW7%B6Yj$!rJD`8VU%aq'
        'enFCU(+eA_4vStB%@8(2!@K+@5;50dytC-CTbBynkF>Mtdm<8A?d><{K84)nGWZ?1n>HFeZudJutQK#iBL6X8WFsc=VC6-(se+ts'
        'VuL@!#xQPZ+Ta+K4WMhmutCxx)Ir0F^jtz6GOSGYVbT%mAEoC?cS=@89X4!?p2tzEhE0&)0kTih_$ky;!=|Z!26e))S@Jtb_BqsP'
        '!w#X28+Mrbk5GQ|sD}+ZiaKl9G1N)Jj-!qlc7ps*q81IaX#P{E#|=A;I&atqsD}(YLvhZcP8qg9d7Y#6EK<Dls3pTLP@W&6UNGz<'
        ')J4OVP!|ldQO_7wLp^PngK8Oe5%q*&mr#!xwoG|kruAGwoipqz<?}J^!!=spCzRK9TIZ*z6~jKG{BEF@4f~wdeUtKB>8?Ko#>BG-'
        '4kJ8g(6(t(4?i4P$|@>yx$nm!0a%KzAHui%^8+cYJL?wNt?;p>!6L&%TPo<Z1EIeQ<ENI_*1`&7U&Pj;r#37R_=*ST?aH0?*43>5'
        'BC&WZtXM?w1Sg5`EuJi?q~mq@U%b*p1sfJREj4)*fu%RBox>U?yX?prIY+G{@))&FvJq*?Gx98)4|0K(<vDqw(<PUrLq5y$3bn3*'
        '!?L{Ib-1y^m%PawxdOk{eQ7G}LsNlhD)-Se)JId1Xetm*qeN4gXd3FHX@Y1PBbq9GG?j^_BGEKRG!=-ZLqyXY(R7e#nkAZMh^A?x'
        'X^Lo?B$^HoO%p`ZIMFmlG*yYF3ehy$N7FFTR3@5AL{pJy8X}qoiKYRfsX#P2M3X}_IYg5~G&w|*Lo_)=lS4E)M3X}_IYg5~G&w|*'
        'Lo_)=lVei(k{VkGRhzuN&5(SZ-CSF}^<UWO{it_7<;k5-xs(;Lu)x`75!Q!au3KoZg0$(0xD#R`8(W7gfS}&mK+a_Id*9)$Q29`v'
        'JObH$XT#Jh3C>x7`Q#s|C$gDc6^iS%yTuR2ekG^mFY=B2P5zp~RqrFrbq*}&Z?XyZF;*HbChEdWce5!s3DdYPpraw&h{Hvm$(n9P'
        'wKjj6>LpBa>3K7_e5vI$YEkOJRqMuL11>fQxl`gKa6BYh#I<hqRqLs~YEXUEwyH1Nu`k+PFSxT^$rG41#_9&PqNVC0{{i-NaTRy8'
        '21lTvaog`Ri9}sJR`t$BZ|8d-C~$kz*8k&*hu+<O2XBP|?oY61;eaI#)(wy#)`7c5{<%lAzdEfa0|SM^|KfZRD%GgFjGPU0j=@bh'
        '1~>5-lrQgs!H5K{@4)(Q+xp}P#3cXTo}Qz15{}mH@b}>Ke$U~(Jw3x$wuY}22ILC<>kTlH?$w9H+J6HhoIIuS3jhE'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

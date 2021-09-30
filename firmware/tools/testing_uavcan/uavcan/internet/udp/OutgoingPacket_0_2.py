# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/internet/udp/8174.OutgoingPacket.0.2.uavcan
#
# Generated at:  2021-09-29 15:15:51.864309 UTC
# Is deprecated: no
# Fixed port ID: 8174
# Full name:     uavcan.internet.udp.OutgoingPacket
# Version:       0.2
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class OutgoingPacket_0_2(_dsdl_.FixedPortCompositeObject):
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
    NAT_ENTRY_MIN_TTL: int = 86400

    def __init__(self,
                 session_id:          _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None,
                 destination_port:    _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None,
                 destination_address: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None,
                 use_masquerading:    _ty_.Optional[bool] = None,
                 use_dtls:            _ty_.Optional[bool] = None,
                 payload:             _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None) -> None:
        """
        uavcan.internet.udp.OutgoingPacket.0.2
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param session_id:          saturated uint16 session_id
        :param destination_port:    saturated uint16 destination_port
        :param destination_address: saturated uint8[<=45] destination_address
        :param use_masquerading:    saturated bool use_masquerading
        :param use_dtls:            saturated bool use_dtls
        :param payload:             saturated uint8[<=508] payload
        """
        self._session_id:          int
        self._destination_port:    int
        self._destination_address: _np_.ndarray
        self._use_masquerading:    bool
        self._use_dtls:            bool
        self._payload:             _np_.ndarray

        self.session_id = session_id if session_id is not None else 0

        self.destination_port = destination_port if destination_port is not None else 0

        if destination_address is None:
            self.destination_address = _np_.array([], _np_.uint8)
        else:
            destination_address = destination_address.encode() if isinstance(destination_address, str) else destination_address  # Implicit string encoding
            if isinstance(destination_address, (bytes, bytearray)) and len(destination_address) <= 45:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._destination_address = _np_.frombuffer(destination_address, _np_.uint8)
            elif isinstance(destination_address, _np_.ndarray) and destination_address.dtype == _np_.uint8 and destination_address.ndim == 1 and destination_address.size <= 45:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._destination_address = destination_address
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                destination_address = _np_.array(destination_address, _np_.uint8).flatten()
                if not destination_address.size <= 45:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'destination_address: invalid array length: not {destination_address.size} <= 45')
                self._destination_address = destination_address
            assert isinstance(self._destination_address, _np_.ndarray)
            assert self._destination_address.dtype == _np_.uint8
            assert self._destination_address.ndim == 1
            assert len(self._destination_address) <= 45

        self.use_masquerading = use_masquerading if use_masquerading is not None else False

        self.use_dtls = use_dtls if use_dtls is not None else False

        if payload is None:
            self.payload = _np_.array([], _np_.uint8)
        else:
            payload = payload.encode() if isinstance(payload, str) else payload  # Implicit string encoding
            if isinstance(payload, (bytes, bytearray)) and len(payload) <= 508:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._payload = _np_.frombuffer(payload, _np_.uint8)
            elif isinstance(payload, _np_.ndarray) and payload.dtype == _np_.uint8 and payload.ndim == 1 and payload.size <= 508:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._payload = payload
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                payload = _np_.array(payload, _np_.uint8).flatten()
                if not payload.size <= 508:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'payload: invalid array length: not {payload.size} <= 508')
                self._payload = payload
            assert isinstance(self._payload, _np_.ndarray)
            assert self._payload.dtype == _np_.uint8
            assert self._payload.ndim == 1
            assert len(self._payload) <= 508

    @property
    def session_id(self) -> int:
        """
        saturated uint16 session_id
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._session_id

    @session_id.setter
    def session_id(self, x: _ty_.Union[int, _np_.uint16]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 65535:
            self._session_id = x
        else:
            raise ValueError(f'session_id: value {x} is not in [0, 65535]')

    @property
    def destination_port(self) -> int:
        """
        saturated uint16 destination_port
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._destination_port

    @destination_port.setter
    def destination_port(self, x: _ty_.Union[int, _np_.uint16]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 65535:
            self._destination_port = x
        else:
            raise ValueError(f'destination_port: value {x} is not in [0, 65535]')

    @property
    def destination_address(self) -> _np_.ndarray:
        """
        saturated uint8[<=45] destination_address
        DSDL does not support strings natively yet. To interpret this array as a string,
        use tobytes() to convert the NumPy array to bytes, and then decode() to convert bytes to string:
        .destination_address.tobytes().decode()
        When assigning a string to this property, no manual conversion is necessary (it will happen automatically).
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]) -> None:
        x = x.encode() if isinstance(x, str) else x  # Implicit string encoding
        if isinstance(x, (bytes, bytearray)) and len(x) <= 45:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._destination_address = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 45:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._destination_address = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size <= 45:  # Length cannot be checked before casting and flattening
                raise ValueError(f'destination_address: invalid array length: not {x.size} <= 45')
            self._destination_address = x
        assert isinstance(self._destination_address, _np_.ndarray)
        assert self._destination_address.dtype == _np_.uint8
        assert self._destination_address.ndim == 1
        assert len(self._destination_address) <= 45

    @property
    def use_masquerading(self) -> bool:
        """
        saturated bool use_masquerading
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._use_masquerading

    @use_masquerading.setter
    def use_masquerading(self, x: bool) -> None:
        self._use_masquerading = bool(x)  # Cast to bool implements saturation

    @property
    def use_dtls(self) -> bool:
        """
        saturated bool use_dtls
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._use_dtls

    @use_dtls.setter
    def use_dtls(self, x: bool) -> None:
        self._use_dtls = bool(x)  # Cast to bool implements saturation

    @property
    def payload(self) -> _np_.ndarray:
        """
        saturated uint8[<=508] payload
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
        if isinstance(x, (bytes, bytearray)) and len(x) <= 508:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._payload = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 508:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._payload = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size <= 508:  # Length cannot be checked before casting and flattening
                raise ValueError(f'payload: invalid array length: not {x.size} <= 508')
            self._payload = x
        assert isinstance(self._payload, _np_.ndarray)
        assert self._payload.dtype == _np_.uint8
        assert self._payload.ndim == 1
        assert len(self._payload) <= 508

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: OutgoingPacket_0_2._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.add_aligned_u16(max(min(self.session_id, 65535), 0))
        _ser_.add_aligned_u16(max(min(self.destination_port, 65535), 0))
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.destination_address) <= 45, 'self.destination_address: saturated uint8[<=45]'
        _ser_.add_aligned_u8(len(self.destination_address))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.destination_address)
        _ser_.add_unaligned_bit(self.use_masquerading)
        _ser_.add_unaligned_bit(self.use_dtls)
        _ser_.skip_bits(6)
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.payload) <= 508, 'self.payload: saturated uint8[<=508]'
        _ser_.add_aligned_u16(len(self.payload))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.payload)
        _ser_.pad_to_alignment(8)
        assert 64 <= (_ser_.current_bit_length - _base_offset_) <= 4488, \
            'Bad serialization of uavcan.internet.udp.OutgoingPacket.0.2'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: OutgoingPacket_0_2._DeserializerTypeVar_) -> OutgoingPacket_0_2:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "session_id"
        _f0_ = _des_.fetch_aligned_u16()
        # Temporary _f1_ holds the value of "destination_port"
        _f1_ = _des_.fetch_aligned_u16()
        # Temporary _f2_ holds the value of "destination_address"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 45:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 45')
        _f2_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len0_)
        assert len(_f2_) <= 45, 'saturated uint8[<=45]'
        # Temporary _f3_ holds the value of "use_masquerading"
        _f3_ = _des_.fetch_unaligned_bit()
        # Temporary _f4_ holds the value of "use_dtls"
        _f4_ = _des_.fetch_unaligned_bit()
        _des_.skip_bits(6)
        # Temporary _f5_ holds the value of "payload"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len1_ = _des_.fetch_aligned_u16()
        assert _len1_ >= 0
        if _len1_ > 508:
            raise _des_.FormatError(f'Variable array length prefix {_len1_} > 508')
        _f5_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len1_)
        assert len(_f5_) <= 508, 'saturated uint8[<=508]'
        self = OutgoingPacket_0_2(
            session_id=_f0_,
            destination_port=_f1_,
            destination_address=_f2_,
            use_masquerading=_f3_,
            use_dtls=_f4_,
            payload=_f5_)
        _des_.pad_to_alignment(8)
        assert 64 <= (_des_.consumed_bit_length - _base_offset_) <= 4488, \
            'Bad deserialization of uavcan.internet.udp.OutgoingPacket.0.2'
        assert isinstance(self, OutgoingPacket_0_2)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'session_id=%s' % self.session_id,
            'destination_port=%s' % self.destination_port,
            'destination_address=%s' % repr(bytes(self.destination_address))[1:],
            'use_masquerading=%s' % self.use_masquerading,
            'use_dtls=%s' % self.use_dtls,
            'payload=%s' % repr(bytes(self.payload))[1:],
        ])
        return f'uavcan.internet.udp.OutgoingPacket.0.2({_o_0_})'

    _FIXED_PORT_ID_ = 8174
    _EXTENT_BYTES_ = 600

    _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{`t?O>7)TcIL>kM7JbcKeqgDm1$chz2s;_krGA!#Iz{KN@-+5e{d2wvo+l{(=GPjc6ARq1_F2w3G85iOtKSTkGTZM'
        'F~=Nz%rVCt_Y@>pz}R3BWP#+6_o}M9t7nFktsf*CM}Vkdch##`?|tvDUX8vy_*ehDIV1lJ&cuC3IDWk)c;YeN`+~K7UT@h^5J$pG'
        '`Dk!#llxu(AD!F%n2&xoTKMVck4N)^LoF{1c`|Zm2FGrtNoJ>6!mC4`Y=tZU5_1{r*(|JkVak(`r}fN<>z`(6H}b;n7PGf`IvUKj'
        'dOQ(c6e7jLclGC=jpz(L@Ta4njs{0sEKL)youyoiJ_qu9@Lr4>4W9hi<GxceWVIZYvQ~;*?lnD5aJOC$Mx4463a=Y-=Nd5H<w<pS'
        'M_O$!ZTURxrtXLy2jVspX)A~vK5}0ioZiX_;k5b{c-O>NxT8NA-5d>`ZHbhH4oe)9&{tX8wFZ{p0{7qYoYCN5%ZcpKXV+^pGq+t&'
        'kPdE&zz4xol17Auge5>CVM(9#n4fXd?vvEz1RjL~m`Fj+B!tz87m_G(c!KlVoZy!6W580|l~WQf;wTi{+VN8L#E)#|`+c&_<CNGD'
        'h+;RbliTp7lZAE)T#~2*BTdeFUXo^Vmgn#=^?(8{le#R$!FM*d&RyFgag?N1m<4T6Hd4fil6?RRa;NwA1y3R(ScfCIj^s)3&?)xh'
        'L|nk9l(?+NNs#%e7sIwRs{%+^jwetCnI~KzobGTQ)<+=e=aeqp7u=Wir`PCl_l*07`=(OFafjnfhTCi*za#hT;1%GX7%${Th}uY%'
        '?BL}+Fq$N+KN>uLm%&qba$PEa1D{qwcC5vH9)JiHXbm=J3pNK&0rFyIdue|}mj)*_lv+|7Q|G--YY0I#`(Uf>i_ze0&S?ooU^*TD'
        'eKa`wk(VldZ^5sc)4>z1C>{;SUPMGcXh*(hgHbhk5P=*}aG%CJVQG|@Ud47jFj@EN;JGVNXtR`uQ-|WFab&_nbOtc~nH!n!g9%KG'
        'Jk*k?8vXfbp3V+M+x=ZFjNgM<&);NWm*3<uPrbcZ+HM7G7eosaZpw%5ot&1GU*Lsc)c660HQn0aFnWQ^XE>kMaO}*G9?<_jA^)W{'
        'dSFNo>Ss?D&*&5M;E*0tzaPNQhb!;sll0J#&gywjO}wLrfiG$m^Wh2neq`!6`V_T>^r(6_i)$U*a~wTFj}Gb66}s>go;|bg9D0mC'
        'J*3C=8bf;GzN6_g^!SjToLC9o!1GhzX+AwcPY&s`YV1LHe-!6F_nqg`Q}o#(Jw25Ncnj~I|6a7{bM*9(zK}~AczN-A&!^AR7l!nu'
        'J$Zr=@c!ioqDx<-FAeD{6?ws1p!ezn)1xobSBCVpeffn^Fy_odtwCR<uMH_FWQ$zC{?HWZ8A^t9PSGLz@sF#&@krLAuhY39eKTLv'
        '&;v^8tw**7eS^L^q-XD|8JIy}G>m=wk*-bOqGyM6KHsO-*}@}VgT77YhxDEAyib?`<A3y6_@E2)ogrN;b^9jJoHzBm^w`#=Kcb66'
        'TK`^hfLSo-+@t5I;D|2K`j9qC6wE6eoPV%2t1DJzP^?GK(Z-N2e{V^^Oqh3JZ_cWGRV7iCLsc^cSM)qx9@3Rbd@KUZMvjryDhE}`'
        'ROM3DL{$$JWEAUPpesXq@quJRmvQc;N%>UuR@GV+Cnicvj7Z5KZ*+A?*Q#h~AYLx#9Gg0+Vx@`{6DKB042-Dt=tX*ot_|t>1Iq*`'
        '!2EYhxlE$Q#Egj;6E7xOG*%>kz#Y9z*N61Iy>YVwG}jP2@8?{Y$T4waqQ=CGiI_3GC<y@%@6z{%^n-_z6J19dzcY>@6G0|^O!V9z'
        'J5o-H%MT|o1Ukx~eCN9{l*@SPphkSzoT<T}ubQ(p7&mMluffotH(#j1+`n#;8chG&=6nq({9UtAgC+jHxmKee(r=m{*61hnADW-k'
        '=obCQ=2ne<M*pe#S&jaf{(}Cd`QsXO>AygoKx6tVx;xC;9EuVKm07zP*IfIzrf8VOWbrW<4YSDc558!?6lv!Fi-yNiG)UP#@}hy<'
        '&k;U`qJdQP@PD>wAZ4NVgDDzt&u>cY{&o}%kBK9rXiz9Hi-w0?^YIl8--WY>D;lc!m@FC|Psy<Sh>C`XFB#6>r)bF0(olGjMZ<S5'
        '8D9DyDjKGj3{OA8qCv%s{fmZi?ELR68Xk4YusTsRpsZBBpo<3gZ{RUj318A#tP;MWkhMacfHeY?3J+5!V3qJ2qfUUzK$Z&Fa&WD|'
        'DYGxd94FyIjNG%I{n^2pnawC*UP!R_N}_~Z+ah`Z*>QQoWdki{eLrFj5pI<E4mR65QL@7lhdU&V>eh`Y<*HrRPGB5%HghUm5C&A3'
        '??*c@8c8nVY{GY05c}}U^6F~c{A+!b)4-mcY%B&${3PQElU+O>Vh_wAJ5jPNRDTb7-(h{i1j$10zEjubENs07mh1`YeWh$0yNQWx'
        'a@sBnL+&Hz*ct6~JR5eBcs(QpJ4F&v%tPQrHuO446c85niHNeq=Bk0oRnHMcV<j9I5h;u}d8%8gHwvpbh9*=u3`X{4uafWD940QW'
        'ULcX3@>DDmX4_FBccoX_ym5<&nA;w3Dm7iV?rhw>vT=iW*q%p45RoPx%ujOqvR7Ye^CsNMY^C*p2T=k-4V^*&?F`1j=ui%5XJVbK'
        'tfHtAhGa$Es{D%0T^z`QC<|pTSH#TLP=R+S5-*V;g3mGFg@>tbBZplO7Kl~|58KWFnE(l}5FpySn8VAOR}WT}0v5+W$$Ys`Cs!59'
        '#JWYu9MH&uy1rfzCEYo)@1G@8BRK#3<>mVMi);1s_4D_cs^=qP1*bq@xzRYk-f-G$>uam*!g>S#s2^)=nXfl4TxzUex^Q7-&LmLm'
        'W>KL81yRr{NGS^A1jd;$Xi1v^dtvRU2Sx}MfEY$0&x0O1JOQ;V;5r*0UD;gU^G6|)Rrq_kF{d|eYQx~0%$vAdtYT-O+G2lkaO9&X'
        '@;M7DJ#P0kT2sC3uT{%E6TD>_6t>(quI_>%qy+D8kT$co$-GzR^+iCske5$N2Y}E667s=~joaV@0Bs9n?f!44uRV)vJE@Ppbnr)a'
        'fXXH;*iBeKZsT1F=@+iEK3LW*ZfA*?_UmLbiDK<k@hS`6QP{kF{T7-7TDr($oW`BH^=T}x3v_(e6_TM-gQHuZK-gsUri%N*;HBv|'
        '2YL}+37NeM|CmyQjT{oVgBjrb-htZ8Ol7;v`qS#v3k2?3^S^5D<*_>u@2htoxEpGPO`~sqT|N2~JMU&o{CKs!{s;Qg=SY8A^W0^0'
        '#%(u$@l5s9OP^Fhe7%t$jva?#zuIq@4vdF&WJ3jhd$rR6(0IKf-sxK=5=A>6V0bL>=_@b+Mn5+KZ`I>T8(ePyo_BLgD_AIRhxbd+'
        'mw-!^{x2k}jWyElr{I^tt>qCG9X_n$07%e&+89p2Q1My@j<f722xN$p&_MSY<9&}hxrsK5Jl*{G3b}OoymZ^kD;FCw*urvNxa9B{'
        'Y%k$GkMC$e&0dK@yjYYPU@|mI%-by|z&=`6Z`{85`>p1+8?D>7uVW7J0ifp(1&94PpIc37QW*18*f$;gHs^8G%pe{^Ji?(qN?kIV'
        'LTJMDLEaE5;|2&7yi^wYn3w<&OA&xE;J%WMOfJy8A!+e!7lODl>3${okWnUp33`o$+rWX}M+e{(%m9%N>j5ty?vU?*RHKlKI@xb;'
        '#^orC%K^9+2B0W*bH33q=~tvs2aFG1&Fz=(Vi?48<;vx<*_%@1%r8v%&fuvIdQNyM;Qhz?GrS)>xpr}-(HP;S9mF{woH8!Mwc34k'
        '(GE5ImV4S=bm!fFb?ffGxxaM(!~ONWIZ)`mC-BER_~R^khryASgYg+}*f^uF2T!*;-Y$3K9VfhX*8KL&;6zJhKJd!tt(c|mXb_%D'
        'gZNyZZD;8c?r-UfAY57QHT-jN*7iNSmGExnBhm7%oq*s0X;N}d1?qG8J-~CB6Q5f<e`#gxGGM(?U)Di=1Uq$^fW;HM1O>jZ=h=Mp'
        'HNf=WpV#-{0+252$~;f1!?aYD!>OE2=Q#2{8)iCEw-syGBd%%wFnea?`o@jAWo?9gMMd6CD|6yv_52PTZWzadb5Y2W&H~|um$VR4'
        'FtTd&#Z|kBh4VaCfPb?=-RiQQT2WZ$lF~b9S60dJwNvv#$CJ8NJH^p5m}Nqy(Yt^(FdMK7DLzL>Ju3!d$#*CtF6JAa0xk%bb<tO;'
        'U3en58;ntqYt+fD3@lekA@{a<CL)C|thu1H!8s7yHJL?n8SHTo%1-)A(FX(tnvS~YSNL7zx}*c^GtZZHXkBH%fbj}1O=36}ih*2S'
        '96V0H*eB%Af^*2Il;@EvLZy`@@<OAXa1f&<nR0kH;ZmXMzE>iX?a*PNt+MP6%Y3}U=tC+K+FV_mG!d8ADOg2ya6_fvv0?}rJb@))'
        'j}AQ2nRA~wS?p_N=2%cbcRUDqXefEfQj~1cljf?E#Pc*fCx%`J2Bk@a<${x6A<eI9CQ%yMkq^QV-0#SZpdU^QmzeHEBx?7(C=(VW'
        'Wx!w8%ki&obaF`Dqkc)<5XHJ>VNSbY+j!433Vk)A<0U{^ZxeRW4N*#k1oC^Mkeq@|+HUT{^|E>gSS4|WNjAwPo=0z~$AG6y<^&<c'
        '4_FDnfT3$V834pM94s{OLX}?TQU*=SatlmJt^t7HiW!@Ovv<&*piUWMRh7GKEQ)Y7(6twVkxJu({2grv()m<g08NwrqAK6z0{I<S'
        'u+HN4t1=o{u;!O|p?Z@--AW?dm#lnq#2_MUKa=(5-r{6JWPvG7Qy$<mgk*=wN)&uEPZkj>xR@-eVZA~Ix>^>>_asrzlWP~eqIgki'
        'ISWaGH#5<{$Tgtk^*xgl8-4|(V}7OAFb$&=0Z~4sG_i8>+lqZX)@yq{B=jn&5Ru>0M<uzXu%PXAGnw*lggMdy1Ab=sKc?_oKv&5J'
        'PZ<oRqzE*WWk_Oao|Hi3hz)~81M8rVk>?i?I4(c|j0Q=Yz9wKHQ?er3^7`ZOf^`CPupJY*(kUw7?4e`n{Sa!(Qi}R(QMySNH4O8C'
        'VGrX6;Lz*zt+E!=$yGbbR00UNj*5lAnMzxPG$ht%G++d>tW0o+qDao=;g8E@c(#h@Aem9J)edlsd*yFaZo8oe;6uBdLKqac9Y#Bt'
        'P(yl{qTD2S1s<I>jY4!0<MKQ>jV=%2k-tE0sNrNoAF#<H(O2<s9`eBj#eo!y)~N-{>0K&67(hWRD+a;UMSTosky4W#B?>c=QCT;F'
        '3+i}yM%Ct!1EWUwyV9Qra#7l$6qF$(WsqfNlxHoV9_1^ou_9@)s@rKrfz1<D8|98wAt2IeUdfiq5v*by2Iw?GQW&q4hDHAElCk80'
        '%oQ2;oOX^nl4D|y27urKBMUHaTe-(K3KHBGRuWRUSb)n@r6s8|B@CHMmbd#Aba(JnQl}8oG~~(Q_}-+T>(c(WU?x^^E0@+TEo!Gy'
        '(u6&OX#=4=Dw?@WmPVjSPksfXUNDF6mac8)Few$M7=(<O6bEk;j43jA<u@%f0rka=@=GV<Ad^8PPd}t1h|r(vPz8mA{yv6IpwU<J'
        'A~OVx-X3=d(?BCbX0?>;S4+r=a+Rnu74i)TX1Onwb>M`Rt71y(t}s79Uy*<1hok8F(Km`*HYML^2z=LN8J_t{2k40@rDy~MaT|Gg'
        '$XNo>CRsGVrXT=bvyZEowJQP(1ojE*so<!MmKjw|Uep*iyf}^<g?-!Q_V!qXo*xZcm25^?k5->PWR@k8bf{$(!}jVJ5FJ>Gg>rkt'
        '<U~0m%sKX>C!ord#k)Q$ku;fhWccl(2*RBtVVOJi)KO$n_(-b7QI74!GEI<URk5RzCs|06Ph@I+Erf!sEI*4NsRwysFVdwNo>~Yr'
        'sR@ZIw~k-7s(@kAi)&ni4y`fG1OQ17f;Wg@9x8hcFwE_8TUpS_k=!&7MV9a~Y?}tAiWZpJ#)B2HjolSlWtIU-NZZm`)L5wsDwF5+'
        'n3VX4541vfo`nfosVc5Eib~Lj<g`L4ulDj_<a*&GkA{$pu$fzp3_xLIX+A=(56{rIpp|yCG9#T;6_svP+LJo0lPxqj9Zj$nlBhw4'
        '=at`P!@5&XRe-`8TRJ0Ec#a*u<<4S?<I(vr7`1ucgar}vMVayB4H?L(Vwr1r9l2@rG-j6IaG&+1uT7Mp;Ae0SRvGFg_qxG^O#LK_'
        'Qifg_!c`UoEb+d8QcCVgelt&Q5XQThaFfWkGms$qQ*E32&`!&@^kVv~DzDt~kg2?fG>YP&M2wx3pfsz8KIJJ$esTfuM**lDy{y&?'
        'S2LEpPSk2LG-Ek5mb7v`ywXU-+)7tVSJi1iY1(CTEcacSfZmWSXp|boJ|a?08w`bJUr;v9WVPX#$Dx()7v}w2RW+&P$Y8+ATS77%'
        'frUDK)m1B-L*wVDGS7mTYk1#nPdeSbIR%j#y=3eM>FgOEm8a(l1lYQ?!BZg4{1g`Hx^mTmRY>^NQBRnHW5aKDR&s_S0g;tb)d`NV'
        'IH5+BP(kF=Aw;=RP&;Bi1Y1=ec%1R___kmYCd)EhO~^&dcfC9TkVjQsQpN_%a+O9Qj^O+-GD+yE#R9lH#S<p|;1iU~){M2e&9IY&'
        '=SwO%kzF?By;T63a_n6YSLbz*jR2AsGy_p*JRLx0W1rbYgh0zu42=o8uuC!7Gbu6&$H0iTrwx7fAA_-j4jj;-osJb?_=R&HXcQS4'
        '+U-OFR@k3vf2g2sDLA1ISyWL&B|i)zaS*3wRmr9&hGT7a*+4CAjrrXu0m%f#@gy)2L97n-{_|!d=7H#Wibi3acsLW(2CMq2fNh&s'
        'A&S#G^CWlCGQ0QkFqOy?b9uC9bEPKS3iFo`b4BPV{ZyUY$z84Mbum+~@`8PQ3!II&ji#px$5{3o<k`5!U4Ar?pJt|Rf`%Le#tk4&'
        'IW&yIrFMk*7+PhtSBpz#6eSBi5Q^U~<5nbiwZ73gX?--kCwX=7jP9jQe1{j_PVZe7Pw#EkW@dgkgU5TegV|QBWH+L<O!r&iuMLB+'
        'xjHdHHDw75BE_J4U&0c4di9O_i5frewwuG+)Cps+Dht+%1s7n{UrZ-3_G%9T@4%?PoK9fuRfWKzf<OaC{d_us@mI&-m74S+y!q<H'
        '*reHP$}82yc8|D6-Q(^F)Zl4%-mSa8bbsysr|RKh`;Onc1V6t|zwh2<`1$p{b@<u*_RPI^@x^=i<9&SYp1p@%-@)M)-vxV5N6l|e'
        '4o<fm{a=41Ef*pm{4@Ta36KZ8CqVYPC-B*U{q6~Ta}ouW_x*)&J%HdXf+=rta{a#n5&E&_@k9Us'
    )
    assert isinstance(_MODEL_, _pydsdl_.DelimitedType)

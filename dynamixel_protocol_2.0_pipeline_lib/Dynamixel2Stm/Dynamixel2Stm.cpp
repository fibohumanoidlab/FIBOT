/*
 * Dynamixel2Stm.cpp
 *
 *  Created on: Apr 1, 2023
 *      Author: imchin
 */
#include "Dynamixel2Stm.h"


Dynamixel2Stm::Dynamixel2Stm(){

}
void Dynamixel2Stm::begin(UART_HandleTypeDef* SerialObject){
	_serial=SerialObject;
	HAL_UART_Receive_DMA(_serial, _buff_Rx, MAX_BUFFER_Rx);
}
void Dynamixel2Stm::register_ID(uint8_t* id){
	for(uint8_t j=0;j<MAX_N_OF_DYNAMIXEL;j++){
		_listID[j]=id[j];
	}

}



void Dynamixel2Stm::torqueOn(uint8_t id){
}
uint16_t Dynamixel2Stm::_getcrc(uint16_t crc,uint8_t *data,uint16_t len){
	if(len>1){
		for (int i = 0; i < len; i++){
		    crc = (crc << 8) ^ _CRC_16_TABLE[(((crc>> 8) ^ data[i]) & 0xFF)];
		}
	}else if(len!=0){
		crc = (crc << 8) ^ _CRC_16_TABLE[(((crc>> 8) ^ (uint8_t)*data) & 0xFF)];
	}
	return crc;
}
void Dynamixel2Stm::_q_Tx(uint8_t* data,uint8_t len,uint8_t len_Rx_callback,uint8_t feedbacktype){
	for(uint8_t i=0;i<10;i++){
		if(!_flag_Tx[i]){
			memcpy(_buff_Tx[i],data,len);
			_len_buff_Tx[i]=len;
			_len_Rx_callback[i]=len_Rx_callback;
			_feedback_type[i]=feedbacktype;
			_flag_Tx[i]=1;
			break;
		}
	}
}

void Dynamixel2Stm::ping(uint8_t id){
	uint8_t ping[10]={0xFF,0xFF,0xFD,0x0,0x88,0x03,0x00,0x01,0x88,0x88};
	ping[4]=id;
	_crc=0;
	_crc=_getcrc(_crc, ping, 8);
	ping[9] = (_crc  >> 8)& 0xFF;
	ping[8] = _crc & 0xFF;
	_q_Tx(ping, 10,14,F_PING);

}
void Dynamixel2Stm::led(uint8_t id,uint8_t state){
	uint8_t led[13]={0xFF,0xFF,0xFD,0x0,0x88,6,0x00,0x03,65,0,0x88,0x88,0x88};
	led[4]=id;
	led[10]=state;
	_crc=0;
	_crc=_getcrc(_crc, led, 11);
	led[12] = (_crc  >> 8)& 0xFF;
	led[11] = _crc & 0xFF;
	for(uint8_t i=0;i<MAX_N_OF_DYNAMIXEL;i++){
		if(id==_listID[i]){
			_temp_led_state[i]=state;
		}
	}
	_q_Tx(led, 13,11,F_LED);

}





void Dynamixel2Stm::Spin(){
	_readyTx();
	_timeoutcallback_Rx();  // reset flag Tx
	_protocol();
}

void Dynamixel2Stm::_timeoutcallback_Rx(){
	if(!_Can_Tx && ((HAL_GetTick()-_timestampRxcallback)>=TIME_OUT_Rx_Callback)){
		_Can_Tx=1;
	}
}

void Dynamixel2Stm::_readyTx(){
	if(_Can_Tx){

		if(_flag_Tx[_pos_flag_Tx]){
			_Can_Tx=0;
			_timestampRxcallback=HAL_GetTick();
			_countIn=0;
			_coutInto=_len_Rx_callback[_pos_flag_Tx];
			_onfeedback=_feedback_type[_pos_flag_Tx];
			HAL_UART_Transmit_DMA(_serial,_buff_Tx[_pos_flag_Tx], _len_buff_Tx[_pos_flag_Tx]);
			_flag_Tx[_pos_flag_Tx]=!_flag_Tx[_pos_flag_Tx];
		}
		_pos_flag_Tx=(_pos_flag_Tx+1) % MAX_BUFFER_Tx;
	}


}
void Dynamixel2Stm::_countIN(){
	_countIn=_countIn+1;
	if(_countIn>=_coutInto){
		_Can_Tx=1;
	}
}
#define IFSTATEto(check,tt,ff) if(_buff_Rx[_posdatapre]==check){_state=tt;}else{_state = ff;}													\


void Dynamixel2Stm::_protocol(){
	_posdata=((UART_HandleTypeDef)*_serial).RxXferSize-__HAL_DMA_GET_COUNTER(((UART_HandleTypeDef)*_serial).hdmarx);
	if(_posdata!=_posdatapre){

		switch(_state){
			case H1:
				IFSTATEto(0xFF,H2,H1)
				_flagcrc=1;
				_crc=0;
			break;
			case H2:
				IFSTATEto(0xFF,H3,H1)
			break;
			case H3:
				IFSTATEto(0xFD,RSRV,H1)
			break;
			case RSRV:
				IFSTATEto(0,PKG_ID,H1)
			break;

			case PKG_ID:
				for(uint8_t i=0;i<MAX_N_OF_DYNAMIXEL;i++){
					if(_listID[i]==_buff_Rx[_posdatapre]){
						_onId=i;  // on_Id = on index _listID
						_state=N_L;  // grab N of data
						break;
					}else{
						_state=H1;
					}
				}
			break;


			case N_L: // get N_l to grab
				_grabN = _buff_Rx[_posdatapre] ;
				_state = N_H;
			break;
			case N_H:
				_grabN = _grabN | (_buff_Rx[_posdatapre]<<8);
				_state=INST;  // check instruction
			break;


			case INST:
				if(_buff_Rx[_posdatapre]==I_OK){
					_state = ERR;
				}else{
					_state = H1;
				}
			break;
			case ERR:
				if(_buff_Rx[_posdatapre]==0){
					if(_onfeedback==F_PING){
						_onGrab=_grabN-4;  // - inst -crc_l -crc_r
						_countGrab=0;
						_state = GRABN;
					}else if(_onfeedback==F_LED){
						_state = CRC_L;
					}else{
						_state = H1;
					}
				}else{
					_state=H1;
				}
			break;
			case GRABN:
				_countGrab=_countGrab+1;
				if(_countGrab==_onGrab){
					_state = CRC_L;
				}
			break;
			case CRC_L:
				_flagcrc=0;
				_crcIn=_buff_Rx[_posdatapre];
				_state=CRC_H;
			break;
			case CRC_H:
				_crcIn = _crcIn | (_buff_Rx[_posdatapre]<<8);
				if(_crc==_crcIn){
					if(_onfeedback==F_PING){
						ping_result[_onId]=ping_result[_onId]+1;
					}else if(_onfeedback==F_LED){
						led_state[_onId]=_temp_led_state[_onId];
					}
				}
				_state =H1;
			break;
		}




		if(_flagcrc){
			_crc=_getcrc(_crc, &_buff_Rx[_posdatapre], 1);
		}
		_countIN();
		_posdatapre=(_posdatapre+1)%MAX_BUFFER_Rx;
	}
}




/*
 * MPU9265.cpp
 *
 *  Created on: Apr 27, 2023
 *      Author: imchin
 */
#include "MPU9265.h"

bool MPU9265::begin(I2C_HandleTypeDef* i2cObj ){
	_i2cObj = i2cObj;

	uint8_t data[1] = {MPU9250_WHO_AM_I};
	uint8_t q[1]={0};
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,data,1 , 1000);
	HAL_I2C_Master_Receive(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, q, 1,HAL_MAX_DELAY);

	if(q[0] == 0x71){
		return 1;
	}else{
		return 0;
	}
	uint8_t a[2]={MPU9250_PWR_MGMT_1,0x0};
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,a,2,10000);
	a[1]=0x01;
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,a,2,10000);
	uint8_t b[2]={MPU9250_CONFIG,0x03};
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,b,2,10000);
	uint8_t c[2]={MPU9250_SMPLRT_DIV,0x04};
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,c,2,10000);

	uint8_t d[2]={MPU9250_GYRO_CONFIG,MPU9250_GFS_250<<3}; // gyro config
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,d,2,10000);

	uint8_t e[2]={MPU9250_ACCEL_CONFIG,MPU9250_AFS_2G <<3};  // acc config
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,e,2,10000);

	uint8_t f[2]={MPU9250_ACCEL_CONFIG_2,0x03};
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,f,2,10000);

	uint8_t g[2]={MPU9250_INT_PIN_CFG,0x02}; // ena
	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,g,2,10000);

//	uint8_t data[1] = {MPU9250_TEMP_OUT_H};
//	HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,data,1,100);
//
//	HAL_I2C_Master_Receive(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _temp, 2,10000);
//
//	while(1){
//
//	}
}
void MPU9265::_to_send(uint8_t data,uint8_t mode){
	_buff_out[_indexSend][0]=data;
	_modeIn[_indexSend] = mode;
	_indexSend=(_indexSend+1)%10;
}

void MPU9265::_send(){
	if(_indexNow!=_indexSend){

		HAL_I2C_Master_Transmit(_i2cObj, MPU9250_SLAVE_ADDRESS<<1,_buff_out[_indexNow],1,100);
		switch(_modeIn[_indexNow]){
			case 0:
				HAL_I2C_Master_Receive(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _temp,2,100);
				Temp = ((_temp[0]<<8 | _temp[1]) / 333.87 )+ 21.0;
			break;
			case 1:
				HAL_I2C_Master_Receive(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _gyro,6,100);
				_gx=(_gyro[0]<<8) | _gyro[1];
				_gy=(_gyro[2]<<8) | _gyro[3];
				_gz=(_gyro[4]<<8) | _gyro[5];
				Gx= ((float)_gx)*0.007629395;
				Gy= ((float)_gy)*0.007629395;
				Gz= ((float)_gz)*0.007629395;
			break;
			case 2:
				HAL_I2C_Master_Receive(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _acc,6,100);
				_ax=(_acc[0]<<8) | _acc[1];
				_ay=(_acc[2]<<8) | _acc[3];
				_az=(_acc[4]<<8) | _acc[5];
				Ax= ((float)_ax)*0.000061035;
				Ay= ((float)_ay)*0.000061035;
				Az= ((float)_az)*0.000061035;
			break;
		}
		_indexNow=(_indexNow+1)%10;
	}
}
#define MODETEMP 0
#define MODEGYRO 1
#define MODEACC 2
void MPU9265::readTemp(){
	_to_send(MPU9250_TEMP_OUT_H,MODETEMP);
	_send();
}
void MPU9265::readGyro(){
	_to_send(MPU9250_GYRO_XOUT_H,MODEGYRO);
	_send();
}
void MPU9265::readAcc(){
	_to_send(MPU9250_ACCEL_XOUT_H,MODEACC);
	_send();
}
void MPU9265::StartStreamAll(){
	HAL_I2C_Master_Transmit_IT(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _req_all, 1);
	HAL_I2C_Master_Receive_DMA(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _all, 14);

}
void MPU9265::getGyroXYZ(float * gx, float * gy, float * gz){
	_gx=(_all[8]<<8)  | _all[9];
	_gy=(_all[10]<<8) | _all[11];
	_gz=(_all[12]<<8) | _all[13];
	*gx = (float)_gx *0.007629395;
	*gy = (float)_gy *0.007629395;
	*gz = (float)_gz *0.007629395;
}
void MPU9265::getAccXYZ(float * ax, float * ay, float * az){
	_ax=(_all[0]<<8)  | _all[1];
	_ay=(_all[2]<<8) | _all[3];
	_az=(_all[4]<<8) | _all[5];
	*ax = (float)_ax *0.000061035;
	*ay = (float)_ay *0.000061035;
	*az = (float)_az *0.000061035;
}
void MPU9265::getTemp(float *temp){
	*temp = ((_all[6]<<8 | _all[7]) / 333.87 )+ 21.0;
}
void MPU9265::ISR_Tx(){
	HAL_I2C_Master_Receive_IT(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _all, 14);
}
void MPU9265::ISR_Rx(){
	HAL_I2C_Master_Transmit_IT(_i2cObj, MPU9250_SLAVE_ADDRESS<<1, _req_all, 1);

}


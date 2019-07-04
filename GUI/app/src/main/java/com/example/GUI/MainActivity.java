package com.example.GUI;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}
	public void clickMe0_0_0(View view){
	// onClick logic_0_0_0
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_3_0(View view){
	// onClick logic_0_3_0
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
}